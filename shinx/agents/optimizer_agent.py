import json
import re
from typing import Any, Sequence

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import BaseTool

from shinx.prompts.optimizer_prompt import OPTIMIZER_SYSTEM_PROMPT
from shinx.services.llm_factory import get_chat_model
from shinx.shared.models.suggestion import (
    ImpactLevel,
    OptimizationReport,
    Suggestion,
    SuggestionType,
)
from shinx.tools.base import ToolRegistry


class OptimizerAgent:
    def __init__(
        self,
        llm: BaseChatModel | Any | None = None,
        tools: ToolRegistry | Sequence[BaseTool] | None = None,
        max_turns: int = 6,
        verbose: bool = True,
    ):
        # Support LLMService wrapper for backward compatibility or raw BaseChatModel
        if hasattr(llm, "_provider"):
            self.llm = getattr(llm._provider, "llm", llm)
        elif llm is not None:
            self.llm = llm
        else:
            self.llm = get_chat_model()

        self.tools = tools
        self.max_turns = max_turns
        self.verbose = verbose

        # Prepare LangChain tools and lookup mapping
        self._tool_map: dict[str, Any] = {}
        self._langchain_tools: list[BaseTool] = []

        if isinstance(tools, ToolRegistry):
            self._langchain_tools = tools.to_langchain_tools()
            self._tool_map = {t.name: t for t in self._langchain_tools}
        elif isinstance(tools, Sequence):
            self._langchain_tools = list(tools)
            self._tool_map = {t.name: t for t in self._langchain_tools}

    def _log(self, message: str) -> None:
        if self.verbose:
            print(f"[OptimizerAgent] {message}")

    def optimize(self, query: str) -> OptimizationReport:
        self._log(f"Starting investigation for query: {query.strip()[:80]}...")

        messages: list[BaseMessage] = [
            SystemMessage(content=OPTIMIZER_SYSTEM_PROMPT),
            HumanMessage(
                content=(
                    f"Analyze and optimize the following SQL query:\n\n"
                    f"```sql\n{query.strip()}\n```\n\n"
                    f"Use your tools to investigate its execution plan, inspect the schema and indexes of the "
                    f"involved tables, and provide your final optimization recommendations."
                )
            ),
        ]

        # Bind tools to the model if tools exist
        model_with_tools = (
            self.llm.bind_tools(self._langchain_tools)
            if self._langchain_tools and hasattr(self.llm, "bind_tools")
            else self.llm
        )

        final_content = ""

        for turn in range(self.max_turns):
            self._log(f"Turn {turn + 1}/{self.max_turns}: Requesting LLM decision...")
            response = model_with_tools.invoke(messages)
            messages.append(response)

            tool_calls = getattr(response, "tool_calls", [])
            if tool_calls:
                for tc in tool_calls:
                    tool_name = tc.get("name")
                    tool_args = tc.get("args", {})
                    tool_id = tc.get("id") or tool_name

                    self._log(f"Executing tool: {tool_name} with args: {tool_args}")
                    
                    if tool_name in self._tool_map:
                        try:
                            result = self._tool_map[tool_name].invoke(tool_args)
                        except Exception as e:
                            result = {"error": f"Tool execution failed: {str(e)}"}
                    elif isinstance(self.tools, ToolRegistry):
                        result = self.tools.execute(tool_name, tool_args)
                    else:
                        result = {"error": f"Tool '{tool_name}' not found."}

                    content_str = (
                        result.model_dump_json()
                        if hasattr(result, "model_dump_json")
                        else json.dumps(result, default=str)
                    )

                    messages.append(
                        ToolMessage(
                            tool_call_id=tool_id,
                            name=tool_name,
                            content=content_str,
                        )
                    )
            else:
                self._log("LLM completed investigation and returned final recommendations.")
                final_content = response.content if isinstance(response.content, str) else str(response.content)
                break
        else:
            self._log("Reached maximum turn limit. Requesting final synthesis...")
            messages.append(
                HumanMessage(
                    content=(
                        "You have reached the investigation limit. Stop calling tools. "
                        "Synthesize your findings and output ONLY the final JSON OptimizationReport."
                    )
                )
            )
            final_res = self.llm.invoke(messages)
            final_content = final_res.content if isinstance(final_res.content, str) else str(final_res.content)

        # 1. Try parsing directly from the model's final response if valid JSON was returned
        if final_content:
            report = self._parse_report(query, final_content)
            if report.suggestions and report.suggestions[0].title != "Optimization Findings":
                return report

        # 2. Try structured output model if direct parsing was inconclusive
        if hasattr(self.llm, "with_structured_output"):
            try:
                structured_model = self.llm.with_structured_output(OptimizationReport)
                structured_report = structured_model.invoke(messages)
                if isinstance(structured_report, OptimizationReport):
                    if not structured_report.query:
                        structured_report.query = query
                    return structured_report
            except Exception as e:
                self._log(f"Structured output synthesis note: {e}. Falling back to content parsing.")

        return self._parse_report(query, final_content)

    def _parse_report(self, query: str, content: str) -> OptimizationReport:
        cleaned = content.strip()

        if "```" in cleaned:
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
            if match:
                cleaned = match.group(1).strip()

        try:
            data = json.loads(cleaned)
            if not data.get("query"):
                data["query"] = query
            return OptimizationReport.model_validate(data)
        except Exception as e:
            self._log(f"Warning: Failed to parse strict JSON ({e}). Falling back to extraction.")
            match = re.search(r"\{[\s\S]*\}", cleaned)
            if match:
                try:
                    data = json.loads(match.group(0))
                    if not data.get("query"):
                        data["query"] = query
                    return OptimizationReport.model_validate(data)
                except Exception:
                    pass

            return OptimizationReport(
                query=query,
                bottleneck_identified="Analysis completed (see recommendations).",
                suggestions=[
                    Suggestion(
                        title="Optimization Findings",
                        type=SuggestionType.QUERY_REWRITE,
                        impact=ImpactLevel.MEDIUM,
                        confidence=0.7,
                        explanation=content,
                    )
                ],
            )

import json
import re
from typing import Any

from shinx.prompts.optimizer_prompt import OPTIMIZER_SYSTEM_PROMPT
from shinx.services.llm.base import BaseLLMProvider, LLMMessage
from shinx.shared.models.suggestion import OptimizationReport, Suggestion, SuggestionType, ImpactLevel
from shinx.tools.base import ToolRegistry


class OptimizerAgent:
    def __init__(
        self,
        llm: BaseLLMProvider,
        tools: ToolRegistry,
        max_turns: int = 6,
        verbose: bool = True,
    ):
        self.llm = llm
        self.tools = tools
        self.max_turns = max_turns
        self.verbose = verbose

    def _log(self, message: str) -> None:
        if self.verbose:
            print(f"[OptimizerAgent] {message}")

    def optimize(self, query: str) -> OptimizationReport:
        self._log(f"Starting investigation for query: {query.strip()[:80]}...")

        messages: list[LLMMessage] = [
            LLMMessage(role="system", content=OPTIMIZER_SYSTEM_PROMPT),
            LLMMessage(
                role="user",
                content=(
                    f"Analyze and optimize the following SQL query:\n\n"
                    f"```sql\n{query.strip()}\n```\n\n"
                    f"Use your tools to investigate its execution plan, inspect the schema and indexes of the "
                    f"involved tables, and provide your final optimization recommendations."
                ),
            ),
        ]

        tool_schemas = self.tools.to_schemas()

        for turn in range(self.max_turns):
            self._log(f"Turn {turn + 1}/{self.max_turns}: Requesting LLM decision...")
            response = self.llm.generate(messages, tools=tool_schemas)

            if response.has_tool_calls:
                messages.append(
                    LLMMessage(
                        role="assistant",
                        content=response.content,
                        tool_calls=response.tool_calls,
                    )
                )

                for tc in response.tool_calls:
                    self._log(f"Executing tool: {tc.name} with args: {tc.arguments}")
                    result = self.tools.execute(tc.name, tc.arguments)

                    messages.append(
                        LLMMessage(
                            role="tool",
                            name=tc.name,
                            tool_call_id=tc.id,
                            content=json.dumps(result, default=str),
                        )
                    )
            else:
                self._log("LLM completed investigation and returned final recommendations.")
                return self._parse_report(query, response.content or "")

        self._log("Reached maximum turn limit. Requesting final synthesis...")
        messages.append(
            LLMMessage(
                role="user",
                content=(
                    "You have reached the investigation limit. Stop calling tools. "
                    "Synthesize your findings and output ONLY the final JSON OptimizationReport."
                ),
            )
        )
        final_res = self.llm.generate(messages, tools=None)
        return self._parse_report(query, final_res.content or "")

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

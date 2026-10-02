from pydantic import BaseModel, Field
from typing import Any

class PlanNode(BaseModel):
    node_type: str

    startup_cost: float | None = None
    total_cost: float | None = None
    estimated_rows: int | None = None
    estimated_width: int | None = None

    schema_name: str | None = None
    relation_name: str | None = None
    alias: str | None = None
    index_name: str | None = None

    filter: str | None = None
    index_condition: str | None = None
    join_condition: str | None = None

    # plan mode returns hierarchical structure for complex queries
    children: list["PlanNode"] = Field(default_factory=list)

    # those we are not covering
    extra: dict[str, Any] = Field(default_factory=dict)


    # postgres specific normalization
    @classmethod
    def from_postgres(cls, node: dict[str, Any]) -> PlanNode:
        known_fields = {
            "Node Type",
            "Startup Cost",
            "Total Cost",
            "Plan Rows",
            "Plan Width",
            "Schema",
            "Relation Name",
            "Alias",
            "Index Name",
            "Filter",
            "Index Cond",
            "Hash Cond",
            "Merge Cond",
            "Join Filter",
            "Plans",
        }

        return cls(
            node_type=node["Node Type"],

            startup_cost=node.get("Startup Cost"),
            total_cost=node.get("Total Cost"),
            estimated_rows=node.get("Plan Rows"),
            estimated_width=node.get("Plan Width"),

            schema_name=node.get("Schema"),
            relation_name=node.get("Relation Name"),
            alias=node.get("Alias"),
            index_name=node.get("Index Name"),

            filter=node.get("Filter"),
            index_condition=node.get("Index Cond"),

            join_condition=(
                node.get("Hash Cond")
                or node.get("Merge Cond")
                or node.get("Join Filter")
            ),

            children=[
                cls.from_postgres(child)
                for child in node.get("Plans", [])
            ],

            extra={
                key: value
                for key, value in node.items()
                if key not in known_fields
            },
        )
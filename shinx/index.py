import pprint
import json

from shinx.adapters.postgres_adapter import PostgresAdapter
from shinx.services.db_service import DBService

from shinx.shared.models.db_metadata import DBMetadata
from shinx.shared.models.plan_node import PlanNode
from shinx.shared.models.query_analysis import QueryAnalysis

p = PostgresAdapter(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="postgres"
)

query = "select * from members;"

# create a structured input for LLM
db_service = DBService(p)

db_metadata: DBMetadata | None = db_service.crawl()
if db_metadata is None:
    raise ValueError("Failed to crawl database metadata")

exlain_plan: PlanNode | None = db_service.explain(query)
if exlain_plan is None:
    raise ValueError("Failed to explain query plan")

query_analysis = QueryAnalysis(query=query, dbMetdata=db_metadata, plan=exlain_plan)

pprint.pprint(query_analysis.model_dump())
#  Uncomment incase you need to print it
# with open("query_analysis.json", "w", encoding="utf-8") as f:
#     json.dump(
#         query_analysis.model_dump(),
#         f,
#         indent=2,
#     )

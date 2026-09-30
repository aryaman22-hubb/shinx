from shinx.adapters.postgres_adapter import PostgresAdapter
from shinx.services.crawling_service import CrawlingService

p = PostgresAdapter(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="postgres"
)

crawling_service = CrawlingService(p)
crawling_service.crawl()

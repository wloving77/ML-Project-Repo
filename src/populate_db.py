""" This script is run after the database is initialized and populates the database from the giant JSON file in data/"""

from helpers.embedding_helper import EmbeddingHelper
from helpers.scraping_helpers import ScrapeHelpers
from helpers.postgres_helper import PostgresConnector
from dotenv import load_dotenv

load_dotenv("prod.env")

# For running on host machine:
# load_dotenv("dev.env")

embed_helper = EmbeddingHelper()
scrape_helper = ScrapeHelpers()
pg_helper = PostgresConnector()

professors_and_abstracts = scrape_helper.read_json_to_dict(
    "./data/professors_papers_and_abstracts.json"
)

pg_helper.create_connection()
for professor in professors_and_abstracts:
    professor_name = professor["Professor"]
    for paper in professor["Papers"]:
        paper_title = paper["title"]
        paper_abstract = paper["abstract"]
        paper_link = paper["paper_link"]
        if not paper_abstract or not paper_link or not paper_title:
            continue
        paper_embedding = embed_helper.create_embedding(paper_abstract)
        pg_helper.insert_professor_and_paper(
            professor_name, paper_title, paper_abstract, paper_embedding, paper_link
        )
        print(f"Inserted {paper_title} for {professor_name}")

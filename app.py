import json

from apify.postScraper import fetch_linkedin_posts_and_save_db
from clay.linkedin import send_leads_linkedin_to_api

from db.init_db import init_db
from ragSystem.rag_pipeline import rag_pipeline


def run_pipeline():
    # 1️⃣ Initialize DB
    init_db()
    # print("✅ Database initialized")

    # 2️⃣ Fetch posts from Apify → DB
    # print("🚀 Fetching LinkedIn posts...")
    # fetch_linkedin_posts_and_save_db()
    # print("✅ Posts saved to DB")

    # 3️⃣ Process posts and getting the potential users
    # print("Running the RAG pipeline and storing the users in the ")
    # rag_pipeline()
    # print("All leads are added in the database")

    # 4️⃣ Send leads to Clay / calling system
    send_leads_linkedin_to_api()
    print("✅ Lead pipeline completed")

if __name__ == "__main__":
    run_pipeline()

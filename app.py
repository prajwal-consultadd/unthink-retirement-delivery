import os
import glob
import pandas as pd
import json

from apify.postScraper import fetch_linkedin_posts_and_save_db
from ragSystem.pipeline import process_post
from clay.linkedin import send_leads_linkedin_to_api
from db.postgres import init_db


FINAL_DIR = "potentialUsers"


def run_pipeline():
    # Initializing the database
    init_db()
    print("Database Initialized")
    
    # The pipline responsible to fetch post from the apify
    print("🚀 Step 1: Running post scraper...")
    fetch_linkedin_posts_and_save_db()
    print("Post saved in the database")

    # The below pipeline is responsible for running the ragsystem and filtering the potential users
    excel_files = glob.glob(os.path.join(OUTPUT_DIR, "*.xlsx"))

    if not excel_files:
        print("⚠️ No Excel files found in outputs/.")
        return

    os.makedirs(FINAL_DIR, exist_ok=True)

    all_final_leads = []

    print(f"📂 Found {len(excel_files)} Excel files. Processing...")

    for file_path in excel_files:
        print(f"📄 Reading {file_path}")
        df = pd.read_excel(file_path)

        if df.empty:
            continue

        # Iterate row-by-row (each row = one post)
        # print(len(df))
        # count= 0
        for _, row in df.iterrows():
            # print(row)
            post = {
                "post_id": row.get("urn"),
                "post_text": row.get("text"),
                "post_url": row.get("url"),
                "author_profile": row.get("authorProfileUrl")
            }
            # print(post)
            # Skip invalid posts
            if not post["post_text"]:
                continue

            # Apify usually nests comments
            comments_raw = row.get("comments")
            # The comments_raw is often a JSON string in Excel. Normalize robustly:
            # - None/NaN -> []
            # - list -> use as-is
            # - JSON string -> json.loads
            # - single quotes / Python literals (None/True/False) -> try safer replacements
            if comments_raw is None or pd.isna(comments_raw):
                comments_raw = []

            elif isinstance(comments_raw, list):
                # Already parsed
                comments_raw = comments_raw

            elif isinstance(comments_raw, str):
                s = comments_raw.strip()
                # If the string looks like an empty list
                if s == "" or s == "[]":
                    comments_raw = []
                else:
                    # Try standard JSON first
                    try:
                        comments_raw = json.loads(s)
                    except Exception:
                        # Replace single quotes with double quotes for JSON-like strings
                        s2 = s.replace("'", '"')
                        # Replace Python-style None/True/False to JSON null/true/false
                        s2 = s2.replace("None", "null").replace("True", "true").replace("False", "false")
                        try:
                            comments_raw = json.loads(s2)
                        except Exception:
                            # As a last resort, try eval in a very restricted namespace
                            try:
                                comments_raw = eval(s, {"__builtins__": None}, {}) or []
                                # If eval produced a dict (single object), wrap it
                                if isinstance(comments_raw, dict):
                                    comments_raw = [comments_raw]
                            except Exception:
                                comments_raw = []

            else:
                comments_raw = []
            
            # print("Comments Raw is ")
            # if(len(comments_raw)> 0):
                # print(comments_raw)
                # print(type(comments_raw))
                # print(post["post_id"])
                # print(len(comments_raw))
                # count= count+ len(comments_raw)

            comments = []
            for c in comments_raw:
                comments.append({
                    "post_id": post["post_id"],
                    "comment_text": c.get("text"),
                    "comment_url": c.get("link"),
                    "author": {
                        "first_name": c.get("author", {}).get("firstName"),
                        "last_name": c.get("author", {}).get("lastName"),
                        "public_id": c.get("author", {}).get("publicId"),
                    }
                })
            qualified = None
            if len(comments) > 0:
                print("Running the RAG pipeline")
                qualified = process_post(post, comments)

            if qualified:
                all_final_leads.extend(qualified)
        # print(count)
    if not all_final_leads:
        print("⚠️ No potential users found.")
        return

    final_df = pd.DataFrame(all_final_leads)
    print("Potential Users are \n", final_df)
    print(final_df.head())

    output_file = os.path.join(
        FINAL_DIR,
        "potential_users.xlsx"
    )
    # If an existing file is present, read it and append new leads instead of overwriting.
    try:
        if os.path.exists(output_file):
            existing_df = pd.read_excel(output_file, engine="openpyxl")

            # Existing public_ids
            existing_public_ids = set(
                existing_df["public_id"].dropna().astype(str)
            )

            # Keep only NEW public_ids
            final_df = final_df[
                ~final_df["public_id"].astype(str).isin(existing_public_ids)
            ]

            if final_df.empty:
                print("⚠️ No new public_id found. Nothing to append.")
                return

            combined_df = pd.concat([existing_df, final_df], ignore_index=True)
        else:
            combined_df = final_df

        combined_df.to_excel(output_file, index=False, engine="openpyxl")
        print(f"✅ Pipeline complete. Appended final leads to {output_file}")
    except Exception as e:
        # Fallback: try writing final_df alone if anything goes wrong reading existing file
        final_df.to_excel(output_file, index=False, engine="openpyxl")
        print(f"✅ Pipeline complete. Saved final leads to {output_file} (fallback). Error: {e}")
        
    # Running the below pipeline to fetch the user contact from the clay of the linkedin users.
    send_leads_linkedin_to_api()

if __name__ == "__main__":
    run_pipeline()

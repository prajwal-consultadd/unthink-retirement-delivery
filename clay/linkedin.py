import os
import pandas as pd
import requests
import math


POTENTIAL_USERS_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "potentialUsers",
    "potential_users.xlsx"
)

API_URL = "https://api.clay.com/v3/sources/webhook/pull-in-data-from-a-webhook-d8471a01-b33a-4763-b2ac-5cb97ea1e926"  # 🔁 replace with real endpoint
API_HEADERS = {
    "Content-Type": "application/json",
}


def clean_value(v):
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    return v


def send_leads_linkedin_to_api():
    """
    Reads potential_users.xlsx and sends each row
    as a separate API request.
    """

    if not os.path.exists(POTENTIAL_USERS_FILE):
        raise FileNotFoundError(
            f"❌ File not found: {POTENTIAL_USERS_FILE}"
        )

    df = pd.read_excel(POTENTIAL_USERS_FILE, engine="openpyxl")

    if df.empty:
        print("⚠️ potential_users.xlsx is empty.")
        return

    print(f"📤 Sending {len(df)} leads to API...")

    for idx, row in df.iterrows():
        payload = {
            "post_id": clean_value(row.get("post_id")),
            "post_url": clean_value(row.get("post_url")),
            "post_context": clean_value(row.get("post_context")),

            "comment_url": clean_value(row.get("comment_url")),
            "comment_text": clean_value(row.get("comment_text")),

            "author": clean_value(row.get("author")),  # still string, fine

            "intent": clean_value(row.get("intent")),
            "confidence": clean_value(row.get("confidence")),
            "score": clean_value(row.get("score")),

            "public_id": clean_value(row.get("public_id")),
        }

        print("row is ",payload)

        try:
            response = requests.post(
                API_URL,
                json=payload,
                headers=API_HEADERS,
                timeout=15
            )

            if response.status_code == 200:
                print(f"✅ Sent lead {idx + 1}/{len(df)}")
            else:
                print(
                    f"❌ Failed lead {idx + 1}: "
                    f"{response.status_code} | {response.text}"
                )

        except Exception as e:
            print(f"❌ Error sending lead {idx + 1}: {e}")


def build_request_body(row: pd.Series) -> dict:
    """
    Define the API request body here.
    Modify freely based on downstream API (Clay, CRM, etc.)
    """

    return {
        "post_id": row.get("post_id"),
        "post_url": row.get("post_url"),
        "post_context": row.get("post_context"),

        "comment_url": row.get("comment_url"),
        "comment_text": row.get("comment_text"),

        "author": row.get("author"),

        "intent": row.get("intent"),
        "confidence": row.get("confidence"),
        "score": row.get("score"),

        "public_id": row.get("public_id")
    }

if __name__ == "__main__":
    send_leads_linkedin_to_api()
    
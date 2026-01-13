import os
import math
import requests
from dotenv import load_dotenv

from db.postgres import SessionLocal
from db.models.linkedin_potential_user import LinkedInPotentialUser

load_dotenv()

CLAY_API_URL = os.getenv("CLAY_API_URL")

API_HEADERS = {
    "Content-Type": "application/json",
}

def send_leads_linkedin_to_api():
    session = SessionLocal()

    try:
        # 🔑 Only users without phone number
        leads = (
            session.query(LinkedInPotentialUser)
            .filter(LinkedInPotentialUser.phone_number.is_(None))
            .all()
        )

        if not leads:
            print("⚠️ No pending LinkedIn leads to enrich.")
            return

        print(f"📤 Sending {len(leads)} leads to Clay API...")

        for idx, lead in enumerate(leads, start=1):
            payload = {
                "public_id": lead.public_id,
            }

            print("➡️ Sending payload:", payload)

            try:
                response = requests.post(
                    CLAY_API_URL,
                    json=payload,
                    headers=API_HEADERS,
                    timeout=15,
                )

                if response.status_code == 200:
                    print(f"✅ Sent lead {idx}/{len(leads)}")
                else:
                    print(
                        f"❌ Failed lead {idx}: "
                        f"{response.status_code} | {response.text}"
                    )

            except Exception as e:
                print(f"❌ Error sending lead {idx}: {e}")

    finally:
        session.close()


if __name__ == "__main__":
    send_leads_linkedin_to_api()

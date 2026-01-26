import pandas as pd
import requests
from io import StringIO

# from db.postgres import SessionLocal
# from db.models.linkedin_potential_user import LinkedInPotentialUser
from db.postgres import SessionLocal
from db.models.linkedin_potential_user import LinkedInPotentialUser

# 🔗 Google Sheet CSV export URL
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/14fMxl1aUkOsTsVONJHPxEYjMxXek4EO1yqswKMmEamU/export?format=csv"


def sync_google_sheet_to_db():
    print("📥 Reading Google Sheet from Clay...")

    response = requests.get(GOOGLE_SHEET_CSV_URL, timeout=30)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text), dtype=str, keep_default_na=False)

    if df.empty:
        print("⚠️ Google Sheet is empty.")
        return
    

    required_cols = {"Public Id", "Phone Number", "Email"}
    if not required_cols.issubset(df.columns):
        raise Exception(f"Missing required columns: {required_cols}")

    session = SessionLocal()
    updated = 0

    # print("Required columns are ", df.columns)
    try:
        for _, row in df.iterrows():
            public_id = row.get("Public Id")
            print("Public id is ", public_id, " and phone number is ", row.get("Phone Number"), " and email is ", row.get("Email"))
            print(type(public_id))
            if not public_id:
                continue  # safety

            user = (
                session.query(LinkedInPotentialUser)
                .filter(
                    LinkedInPotentialUser.public_id == public_id,
                    LinkedInPotentialUser.soft_delete.is_(False)
                )
                .first()
            )

            if not user:
                continue  # user not in DB → skip

            changed = False

            # Overwrite phone/email from sheet unconditionally (use placeholder if phone missing)
            old_phone = user.phone_number
            old_email = user.email

            phone_val = row.get("Phone Number")
            user.phone_number = str(phone_val)

            email_val = row.get("Email")
            user.email = email_val

            if user.phone_number != old_phone or user.email != old_email:
                changed = True

            if changed:
                updated += 1

        session.commit()
        print(f"✅ Updated {updated} users from Google Sheet.")

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


# if __name__ == "__main__":
#     sync_google_sheet_to_db()
sync_google_sheet_to_db()

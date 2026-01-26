import os
import pandas as pd
from datetime import datetime

from db.postgres import SessionLocal
from db.models.linkedin_potential_user import LinkedInPotentialUser


OUTPUT_DIR = "exports"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def export_and_soft_delete_users():
    session = SessionLocal()

    try:
        # 1️⃣ Fetch users where soft_delete = False
        users = (
            session.query(LinkedInPotentialUser)
            .filter(
                LinkedInPotentialUser.soft_delete.is_(False),
                LinkedInPotentialUser.phone_number.isnot(None),
                LinkedInPotentialUser.phone_number != "",
                LinkedInPotentialUser.phone_number != "No Phone Number"
            )
            .all()
        )

        if not users:
            print("⚠️ No users found to export.")
            return

        print(f"📦 Found {len(users)} users to export")

        # 2️⃣ Convert to list of dicts for Excel
        data = []
        for serial_number, user in enumerate(users, start=1):
            data.append({
                "serial_number": serial_number,
                "post_id": user.post_id,
                "post_url": user.post_url,
                "post_context": user.post_context,
                "comment_url": user.comment_url,
                "comment_text": user.comment_text,
                "author": user.author,
                "intent": user.intent,
                "confidence": user.confidence,
                "score": user.score,
                "public_id": user.public_id,
                "phone_number": user.phone_number,
                "email": user.email,
            })

            # 3️⃣ Mark user as soft deleted
            user.soft_delete = True

        # 4️⃣ Save to Excel
        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(
            OUTPUT_DIR,
            f"linkedin_potential_users_{timestamp}.xlsx"
        )

        df.to_excel(file_path, index=False, engine="openpyxl")

        # 5️⃣ Commit DB changes
        session.commit()

        print(f"✅ Exported users to {file_path}")
        print("✅ soft_delete marked as TRUE in DB")

    except Exception as e:
        session.rollback()
        print("❌ Error:", e)

    finally:
        session.close()


if __name__ == "__main__":
    export_and_soft_delete_users()

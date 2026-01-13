from sqlalchemy.dialects.postgresql import insert
from db.postgres import SessionLocal
from db.models.linkedin_potential_user import LinkedInPotentialUser


def upsert_potential_user(data: dict):
    session = SessionLocal()
    try:
        stmt = insert(LinkedInPotentialUser).values(**data)

        stmt = stmt.on_conflict_do_update(
            index_elements=["public_id"],
            set_={
                "post_id": stmt.excluded.post_id,
                "post_url": stmt.excluded.post_url,
                "post_context": stmt.excluded.post_context,
                "comment_url": stmt.excluded.comment_url,
                "comment_text": stmt.excluded.comment_text,
                "author": stmt.excluded.author,
                "intent": stmt.excluded.intent,
                "confidence": stmt.excluded.confidence,
                "score": stmt.excluded.score,
                "phone_number": stmt.excluded.phone_number,
                "email": stmt.excluded.email,
            },
        )

        session.execute(stmt)
        session.commit()

    finally:
        session.close()

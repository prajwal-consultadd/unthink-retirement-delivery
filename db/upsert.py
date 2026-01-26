from sqlalchemy.dialects.postgresql import insert
from db.normalize_linkedin_post import normalize_linkedin_post
from db.models.linkedin_post_model import LinkedInPost
from db.postgres import SessionLocal


def upsert_post(raw_post: dict):
    session = SessionLocal()
    try:
        data = normalize_linkedin_post(raw_post)

        stmt = insert(LinkedInPost).values(**data)
        stmt = stmt.on_conflict_do_update(
            index_elements=["urn"],
            set_={k: getattr(stmt.excluded, k) for k in data if k != "urn"}
        )

        session.execute(stmt)
        session.commit()

    finally:
        session.close()

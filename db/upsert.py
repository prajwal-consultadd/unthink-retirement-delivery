from sqlalchemy.dialects.postgresql import insert
from db.postgres import SessionLocal
from db.models.linkedin_post_model import LinkedInPost


def upsert_post(post: dict):
    db = SessionLocal()

    try:
        stmt = insert(LinkedInPost).values(**post)

        stmt = stmt.on_conflict_do_update(
            index_elements=["urn"],
            set_={
                col: getattr(stmt.excluded, col)
                for col in post.keys()
                if col != "urn"
            }
        )

        db.execute(stmt)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()

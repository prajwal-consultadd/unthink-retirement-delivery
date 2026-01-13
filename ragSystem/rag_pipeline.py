from db.postgres import SessionLocal
from db.models.linkedin_post_model import LinkedInPost
from db.models.linkedin_potential_user import LinkedInPotentialUser
from db.upsert_potential_users import upsert_potential_user
from ragSystem.pipeline import process_post
import json

def potential_user_exists(public_id: str) -> bool:
    session = SessionLocal()
    try:
        return session.query(LinkedInPotentialUser)\
            .filter(LinkedInPotentialUser.public_id == public_id)\
            .first() is not None
    finally:
        session.close()


def get_all_posts():
    session = SessionLocal()
    try:
        return session.query(LinkedInPost).all()
    finally:
        session.close()
        
def rag_pipeline():
    posts = get_all_posts()

    for post in posts:
        if not post.text:
            continue

        # Normalize comments
        comments_raw = post.comments or []
        if isinstance(comments_raw, str):
            try:
                comments_raw = json.loads(comments_raw)
            except Exception:
                continue

        for c in comments_raw:
            author = c.get("author", {})
            public_id = author.get("publicId")

            if not public_id:
                continue

            # 🚫 Skip if already processed
            if potential_user_exists(public_id):
                continue

            comment = {
                "post_id": post.urn,
                "comment_text": c.get("text"),
                "comment_url": c.get("link"),
                "author": {
                    "first_name": author.get("firstName"),
                    "last_name": author.get("lastName"),
                    "public_id": public_id,
                }
            }

            post_payload = {
                "post_id": post.urn,
                "post_text": post.text,
                "post_url": post.url,
                "author_profile": post.author_profile_url,
            }

            qualified = process_post(post_payload, [comment])

            if not qualified:
                continue

            for lead in qualified:
                upsert_potential_user(lead)

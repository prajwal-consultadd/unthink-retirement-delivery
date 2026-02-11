import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from db.postgres import SessionLocal
from db.models.linkedin_post_model import LinkedInPost
from db.models.linkedin_potential_user import LinkedInPotentialUser
from db.upsert_potential_users import upsert_potential_user
from ragSystem.pipeline import process_post


# -------------------------------
# DB helpers
# -------------------------------

def potential_user_exists(public_id: str) -> bool:
    session = SessionLocal()
    try:
        return (
            session.query(LinkedInPotentialUser)
            .filter(LinkedInPotentialUser.public_id == public_id)
            .first()
            is not None
        )
    finally:
        session.close()


def get_all_posts():
    session = SessionLocal()
    try:
        return session.query(LinkedInPost).all()
    finally:
        session.close()


# -------------------------------
# Thread worker (NO DB here)
# -------------------------------

def process_single_comment(post_payload, comment):
    """
    Runs RAG for a single comment.
    This function MUST NOT touch DB.
    """
    try:
        return process_post(post_payload, [comment])
    except Exception as e:
        print("❌ RAG failed:", e)
        return None


# -------------------------------
# Main pipeline
# -------------------------------

def rag_pipeline():
    posts = get_all_posts()
    print(f"📦 Total posts to process: {len(posts)}")

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

        if not comments_raw:
            continue

        post_payload = {
            "post_id": post.urn,
            "post_text": post.text,
            "post_url": post.url,
            "post_summary": post.text,
            "author_profile": post.author_profile_url,
        }

        comments_to_process = []

        for c in comments_raw:
            author = c.get("author", {})
            public_id = author.get("publicId")

            if not public_id:
                continue

            # 🚫 Skip already processed users
            if potential_user_exists(public_id):
                print("User already exist in the db")
                continue

            comments_to_process.append({
                "post_id": post.urn,
                "comment_text": c.get("text"),
                "comment_url": c.get("link"),
                "author": {
                    "first_name": author.get("firstName"),
                    "last_name": author.get("lastName"),
                    "public_id": public_id,
                }
            })

        if not comments_to_process:
            continue

        print(
            f"⚙️ Post {post.urn} → processing {len(comments_to_process)} comments"
        )

        # ⚡ Multithreaded RAG
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(
                    process_single_comment,
                    post_payload,
                    comment
                )
                for comment in comments_to_process
            ]

            for future in as_completed(futures):
                qualified = future.result()

                if not qualified:
                    print("0 potential comments inserted in db")
                    continue

                # ✅ DB writes happen ONLY here (main thread)
                for lead in qualified:
                    upsert_potential_user(lead)
                print(len(qualified), " comments inserted in db")

    print("✅ RAG pipeline completed")


# -------------------------------
# Entry point
# -------------------------------

if __name__ == "__main__":
    rag_pipeline()

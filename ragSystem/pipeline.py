from ragSystem.post_intent import classify_post_intent as get_post_context
from ragSystem.comment_intent import classify_comment_intent as get_comment_decision
from ragSystem.scoring import compute_score

CONFIDENCE_THRESHOLD = 0
SCORE_THRESHOLD = 0


def process_post(post: dict, comments: list[dict]):
    """
    post = {
        "post_id": "...",
        "post_text": "...",
        "post_url": "...",
        "author_profile": "..."
    }

    comments = [
        {
            "post_id": "...",
            "comment_text": "...",
            "comment_url": "...",
            "author": {
                "first_name": "...",
                "last_name": "...",
                "public_id": "...",
            }
        }
    ]
    """

    # 1️⃣ Post context
    post_ctx = get_post_context(post["post_text"])
    post_context = post_ctx.post_context

    qualified_documents = []
    print("Comments are \n", comments)

    for c in comments:
        comment_text = c["comment_text"]

        # 2️⃣ Comment intent
        decision = get_comment_decision(
            post_context=post_context,
            post_text=post["post_text"],
            comment_text=comment_text
        )

        # 3️⃣ Confidence gate
        if decision.confidence < CONFIDENCE_THRESHOLD:
            continue

        # 4️⃣ Score
        score = compute_score(
            intent=decision.intent,
            confidence=decision.confidence,
            comment_text=comment_text,
            post_context=post_context
        )

        # 5️⃣ Score gate
        if score < SCORE_THRESHOLD:
            continue

        qualified_documents.append({
            "post_id": post["post_id"],
            "post_url": post["post_url"],
            "post_context": post_context,

            "comment_url": c["comment_url"],
            "public_id": c["author"]["public_id"],
            "comment_text": comment_text,

            "author": c["author"],

            "intent": decision.intent,
            "confidence": decision.confidence,
            "score": score
        })
    # print("qualified_documents are \n", qualified_documents)
    return qualified_documents

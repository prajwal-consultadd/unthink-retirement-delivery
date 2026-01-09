from post_intent import classify_post_intent as get_post_context
from comment_intent import classify_comment_intent as get_comment_decision
from scoring import compute_score

CONFIDENCE_THRESHOLD = 0.55
SCORE_THRESHOLD = 45


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
                "profile_url": "..."
            }
        }
    ]
    """

    # 1️⃣ Post context
    post_ctx = get_post_context(post["post_text"])
    post_context = post_ctx.post_context

    qualified_documents = []

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
            "comment_text": comment_text,

            "author": c["author"],

            "intent": decision.intent,
            "confidence": decision.confidence,
            "score": score
        })

    return qualified_documents

post_1 = {
    "post_id": "post_001",
    "post_text": """
Most traders fail not because of strategy, but because they don’t understand risk.

I spent years unlearning bad habits:
- Overtrading
- Random entries
- Emotional exits

What finally worked was building a rules-based framework around risk, time, and liquidity.

This isn’t about signals or shortcuts.
It’s about process.

Comment “INFO” if you want to understand how professionals actually think.
""",
    "post_url": "https://linkedin.com/posts/post_001",
    "author_profile": "https://linkedin.com/in/trading-coach"
}

comments_1 = [
    {
        "post_id": "post_001",
        "comment_text": "I’ve been trading for almost a year and risk management is exactly where I keep messing up. This hit home.",
        "comment_url": "https://linkedin.com/comment/001",
        "author": {
            "first_name": "Rahul",
            "last_name": "Mehta",
            "public_id": "rahul-mehta",
            "profile_url": "https://linkedin.com/in/rahul-mehta"
        }
    },
    {
        "post_id": "post_001",
        "comment_text": "Interesting perspective. Discipline really is underrated.",
        "comment_url": "https://linkedin.com/comment/002",
        "author": {
            "first_name": "Ankit",
            "last_name": "Sharma",
            "public_id": "ankit-sharma",
            "profile_url": "https://linkedin.com/in/ankit-sharma"
        }
    },
    {
        "post_id": "post_001",
        "comment_text": "Is this something someone with a full-time job can realistically follow?",
        "comment_url": "https://linkedin.com/comment/003",
        "author": {
            "first_name": "Neha",
            "last_name": "Kapoor",
            "public_id": "neha-kapoor",
            "profile_url": "https://linkedin.com/in/neha-kapoor"
        }
    }
]


output= process_post(post_1, comments_1)

print(output)

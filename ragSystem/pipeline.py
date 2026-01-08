from post_intent import classify_post_intent as get_post_context
from comment_intent import classify_comment_intent as get_comment_decision
from scoring import compute_score

CONFIDENCE_THRESHOLD = 0.6
SCORE_THRESHOLD = 50


def process_post(post_text: str, comments: list):
    """
    comments can be:
    - list[str]
    - OR list[{"text": "...", "profile_url": "..."}]
    """

    # 1️⃣ Post context (Pydantic object)
    post_ctx = get_post_context(post_text)
    post_context = post_ctx.post_context

    qualified_documents = []

    for c in comments:
        # Normalize comment input
        if isinstance(c, str):
            comment_text = c
            profile_url = None
        else:
            comment_text = c.get("text", "")
            profile_url = c.get("profile_url")

        # 2️⃣ Comment intent (Pydantic object)
        decision = get_comment_decision(
            post_context=post_context,
            post_text=post_text,
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
            "profile_url": profile_url,
            "comment": comment_text,
            "intent": decision.intent,
            "confidence": decision.confidence,
            "score": score,
            "post_context": post_context
        })

    return qualified_documents

# post_text= """Most people stare at charts and hope.
# Hope is not a strategy.

# What actually works is understanding how global price movements behave, why certain hours matter more than others, and how risk quietly decides whether you survive or disappear.

# I’ve spent years breaking this down into a structured system:

# How to read price without drowning in indicators

# How professionals think about entries, exits, and position sizing

# How to stop “feeling” the market and start executing rules

# This isn’t about hype, signals, or shortcuts.
# It’s about building a repeatable decision-making process around liquid global markets.

# If you want a skillset that rewards discipline, patience, and math over emotion and luck, this training was built for that.

# Comment “INFO” and I’ll send the details.

# No promises of Lambos.
# Just a framework that actually respects reality."""

# comments= [
#     "this sounds like a serious, process-driven approach. Would like to see how you structure risk and execution.",
#     "Curious how this differs from the usual chart-pattern and indicator-heavy stuff people push here. What’s the edge?",
#     "Interesting perspective. Discipline is definitely underrated."
# ]

# output= process_post(post_text, comments)

# for o in output:
#     print(o)

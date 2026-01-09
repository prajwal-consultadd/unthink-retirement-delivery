INTENT_BASE_SCORE = {
    "STRUGGLING": 60,
    "LEARNING": 55,
    "RETIREMENT_PLANNING": 50,
    "SIDE_INCOME": 45
}

POST_CONTEXT_MODIFIER = {
    "DISCUSSION": 10,
    "EDUCATIONAL": 5,
    "PROMOTIONAL": -5,
    "NEWS": -8,
    "NOISE": -10
}

def compute_score(intent, confidence, comment_text, post_context):
    score = INTENT_BASE_SCORE.get(intent, 0) * confidence

    # Comment quality rules
    quality = 0
    if "?" in comment_text: quality += 5
    if any(w in comment_text.lower() for w in ["i ", "my ", "me "]): quality += 5
    if any(w in comment_text.lower() for w in ["loss", "confused", "struggling"]): quality += 5
    if any(w in comment_text.lower() for w in ["months", "years", "trying"]): quality += 5

    score += quality
    score += POST_CONTEXT_MODIFIER.get(post_context, 0)

    return min(max(int(score), 0), 100)

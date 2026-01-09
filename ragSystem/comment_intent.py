import json
# from langchain.chains import LLMChain
from llm import llm
from prompts import COMMENT_INTENT_PROMPT
from output_parser import COMMENT_OUTPUT_PARSER
from schemas import CommentIntentOutput
# from ragSystem.llm import llm
# from ragSystem.prompts import COMMENT_INTENT_PROMPT

chain = COMMENT_INTENT_PROMPT | llm | COMMENT_OUTPUT_PARSER

def classify_comment_intent(
    comment_text: str,
    post_text: str,
    post_context: str
) -> CommentIntentOutput:
    try:
        commentIntentOutput= chain.invoke({
            "post_context": post_context,
            "post_text": post_text,
            "comment_text": comment_text
        })
        print("commentIntentOutput", commentIntentOutput)
        return commentIntentOutput
    except Exception:
        return CommentIntentOutput(
            intent="NOISE",
            confidence=0.0,
            recommended_action="DROP"
        )

# post_text="""Most people stare at charts and hope.
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

# comment_text= "I know exactly what this is and I’m interested."

# output= classify_comment_intent(comment_text, post_text, "PROMOTIONAL")

# print(output)

# from ragSystem.llm import llm
from llm import llm
from prompts import POST_INTENT_PROMPT
from output_parser import POST_OUTPUT_PARSER
# from ragSystem.prompts import POST_INTENT_PROMPT
# from ragSystem.output_parser import POST_OUTPUT_PARSER

chain = POST_INTENT_PROMPT | llm | POST_OUTPUT_PARSER

def classify_post_intent(post_text: str):
    try:
        postIntentOutput= chain.invoke({"post_text": post_text})
        print("postIntentOutput", postIntentOutput)
        return postIntentOutput
    except Exception:
        # Fallback must match schema
        return {
            "post_context": "NOISE",
            "confidence": 0.0
        }


# output = classify_post_intent("""Most people stare at charts and hope.
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
# Just a framework that actually respects reality.""")

# print(output)

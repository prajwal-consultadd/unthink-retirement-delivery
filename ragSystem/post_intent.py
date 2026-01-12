# from ragSystem.llm import llm
from ragSystem.llm import llm
from ragSystem.prompts import POST_INTENT_PROMPT
from ragSystem.output_parser import POST_OUTPUT_PARSER
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


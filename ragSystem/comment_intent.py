import json
# from langchain.chains import LLMChain
from ragSystem.llm import llm
from ragSystem.prompts import COMMENT_INTENT_PROMPT
from ragSystem.output_parser import COMMENT_OUTPUT_PARSER
from ragSystem.schemas import CommentIntentOutput
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


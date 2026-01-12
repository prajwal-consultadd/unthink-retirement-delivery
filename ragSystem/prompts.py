from langchain_core.prompts import PromptTemplate
from ragSystem.output_parser import POST_OUTPUT_PARSER, COMMENT_OUTPUT_PARSER
# from ragSystem.output_parser import POST_OUTPUT_PARSER

POST_INTENT_PROMPT = PromptTemplate(
    input_variables=["post_text"],
    partial_variables={
        "format_instructions": POST_OUTPUT_PARSER.get_format_instructions()
    },
    template="""
You are analyzing a LinkedIn post only to understand the CONTEXT
of the discussion, not to judge the author.

Classify the post into ONE category:
- DISCUSSION
- PROMOTIONAL
- NEWS
- EDUCATIONAL
- NOISE

{format_instructions}

Post:
{post_text}
"""
)

COMMENT_INTENT_PROMPT = PromptTemplate(
    input_variables=["post_context", "post_text", "comment_text"],
    partial_variables={
        "format_instructions": COMMENT_OUTPUT_PARSER.get_format_instructions()
    },
    template="""
You are analyzing a LinkedIn COMMENT to identify whether
the PERSON WHO COMMENTED shows personal interest in learning,
improving, or planning finances/trading.

Post context:
{post_context}

Post:
{post_text}

Comment:
{comment_text}

Classify comment intent into ONE:
- LEARNING (beginner, asking how, curiosity)
- STRUGGLING (losses, confusion, frustration)
- RETIREMENT_PLANNING (long-term wealth, retirement focus)
- SIDE_INCOME (extra income curiosity)
- SELLER (promoting services, links, coaching)
- NOISE (praise, emojis, generic reply)

Also decide action:
- CALL (clear personal interest)
- NURTURE (early or vague interest)
- DROP (no interest)

{format_instructions}
"""
)

from langchain_core.output_parsers import PydanticOutputParser
from ragSystem.schemas import PostIntentOutput, CommentIntentOutput
# from ragSystem.schemas import PostIntentOutput

POST_OUTPUT_PARSER = PydanticOutputParser(
    pydantic_object=PostIntentOutput
)

COMMENT_OUTPUT_PARSER = PydanticOutputParser(
    pydantic_object=CommentIntentOutput
)

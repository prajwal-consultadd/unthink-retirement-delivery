from langchain_core.output_parsers import PydanticOutputParser
from schemas import PostIntentOutput
# from ragSystem.schemas import PostIntentOutput

POST_OUTPUT_PARSER = PydanticOutputParser(
    pydantic_object=PostIntentOutput
)

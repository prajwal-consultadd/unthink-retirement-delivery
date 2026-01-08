from pydantic import BaseModel, Field
from typing import Literal

class PostIntentOutput(BaseModel):
    post_context: Literal[
        "DISCUSSION",
        "PROMOTIONAL",
        "NEWS",
        "EDUCATIONAL",
        "NOISE"
    ] = Field(description="Context of the LinkedIn post")

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )

class CommentIntentOutput(BaseModel):
    intent: Literal[
        "LEARNING",
        "STRUGGLING",
        "RETIREMENT_PLANNING",
        "SIDE_INCOME",
        "SELLER",
        "NOISE"
    ] = Field(description="Intent of the commenter")

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )

    recommended_action: Literal[
        "CALL",
        "NURTURE",
        "DROP"
    ] = Field(description="Recommended next action")

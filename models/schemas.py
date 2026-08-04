from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(
        min_length=1,
        max_length=100,
        description="Unique session id"
    )

    message: str = Field(
        min_length=1,
        max_length=1000,
        description="User message"
    )


class ChatResponse(BaseModel):
    reply: str
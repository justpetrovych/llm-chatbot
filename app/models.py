"""Pydantic models for request/response validation."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from .config import config


class ChatMessage(BaseModel):
    """Model for incoming chat messages."""
    userMsgId: str = Field(
        ...,
        min_length=6,
        max_length=config.MAX_ID_LENGTH,
        description="Unique identifier for the user message"
    )
    userMsg: str = Field(
        ...,
        min_length=1,
        max_length=config.MAX_MESSAGE_LENGTH,
        description="The user's message content"
    )


class ThinkingBlock(BaseModel):
    """Model for thinking block content."""
    content: str = Field(..., description="Content of the thinking block")
    position: int = Field(..., description="Position in the original text")


class WebSocketResponse(BaseModel):
    """Model for WebSocket responses."""
    status: str = Field(..., description="Status of the response")
    role: Optional[str] = Field(None, description="Role (user/assistant)")
    userMsgId: Optional[str] = Field(None, description="ID of the user message")
    userMsg: Optional[str] = Field(None, description="Assistant's message content")
    assistantMsgId: Optional[str] = Field(
        None,
        description="ID of the assistant message"
    )
    assistantMsg: Optional[str] = Field(None, description="Assistant's message content")
    hasThinking: Optional[bool] = Field(None, description="Whether message has thinking blocks")
    thinkingBlocks: Optional[List[ThinkingBlock]] = Field(
        None, 
        description="List of thinking blocks in the message"
    )

    def to_json(self) -> str:
        """Convert to JSON string, excluding None values."""
        return self.model_dump_json(exclude_none=True)


class HealthCheckResponse(BaseModel):
    """Model for health check response."""

    status: str = Field(..., description="Service health status")
    model: str = Field(..., description="Current LLM model name")
    version: str = Field(..., description="Application version")

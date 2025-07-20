"""LLM service for handling AI model interactions."""

from typing import AsyncGenerator, Optional
from langchain_ollama import ChatOllama
from ..config import config
from ..utils.logging import get_logger

logger = get_logger(__name__)

class LLMService:
    """Service for managing LLM interactions."""

    def __init__(self, model_name: Optional[str] = None):
        """Initialize LLM service with specified model."""
        self.model_name = model_name or config.DEFAULT_MODEL_NAME
        self._llm = None
        self._initialize_llm()

    def _initialize_llm(self) -> None:
        """Initialize the LLM instance."""
        try:
            self._llm = ChatOllama(model=self.model_name)
            logger.info(f"LLM initialized successfully with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM with model {self.model_name}: {e}")
            raise

    async def stream_response(self, message: str) -> AsyncGenerator[str, None]:
        """Stream response from LLM for a given message."""
        if not self._llm:
            raise RuntimeError("LLM not initialized")

        try:
            logger.info(f"Streaming response for message: {message[:50]}...")

            for chunk in self._llm.stream(message):
                content = str(chunk.content)
                if content:  # Only yield non-empty content
                    yield content

        except Exception as e:
            logger.error(f"Error streaming LLM response: {e}")
            raise

    async def get_response(self, message: str) -> str:
        """Get complete response from LLM."""
        if not self._llm:
            raise RuntimeError("LLM not initialized")

        try:
            logger.info(f"Getting response for message: {message[:50]}...")
            response = await self._llm.ainvoke(message)
            return str(response.content)

        except Exception as e:
            logger.error(f"Error getting LLM response: {e}")
            raise

    def is_healthy(self) -> bool:
        """Check if LLM service is healthy."""
        return self._llm is not None

    def get_model_info(self) -> dict:
        """Get information about the current model."""
        return {
            "model_name": self.model_name,
            "is_healthy": self.is_healthy(),
            "provider": "ollama"
        }


# Global LLM service instance
llm_service = LLMService()

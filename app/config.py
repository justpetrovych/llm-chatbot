"""Application configuration."""

import os
from dotenv import load_dotenv
from typing import List


load_dotenv()


class Config:
    """Application configuration class."""

    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # LLM settings
    DEFAULT_MODEL_NAME: str = os.getenv("DEFAULT_MODEL_NAME", "llama3.1")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "app.log")

    # Security
    MAX_MESSAGE_LENGTH: int = int(os.getenv("MAX_MESSAGE_LENGTH", "1000"))
    MAX_ID_LENGTH: int = int(os.getenv("MAX_ID_LENGTH", "50"))

    @property
    def allowed_origins(self) -> List[str]:
        """Get allowed CORS origins based on the environment."""
        if self.DEBUG:
            return ["http://localhost:3000"]

        origins = os.getenv("ALLOWED_ORIGINS", "")
        return [origin.strip() for origin in origins.split(",") if origin.strip()]


# Global config instance
config = Config()

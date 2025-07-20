"""Application entry point."""

import uvicorn
from app.main import app
from app.config import config
from app.utils.logging import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting server on {config.HOST}:{config.PORT}")

    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        log_level=config.LOG_LEVEL.lower(),
        reload=config.DEBUG,
        access_log=True
    )

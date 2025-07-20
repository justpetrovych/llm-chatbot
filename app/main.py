"""Main FastAPI application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from .config import config
from .models import HealthCheckResponse
from .services.llm_service import llm_service
from .utils.logging import setup_logging
from .utils.template import load_cached_template
from .websocket.handler import handle_websocket_connection
from .websocket.manager import connection_manager

# Initialize logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(fa_app: FastAPI):
    """Application lifespan event handler."""
    # Startup events
    logger.info("Starting Simple AI Chatbot")
    logger.info(f"Model: {config.DEFAULT_MODEL_NAME}")
    logger.info(f"Debug mode: {config.DEBUG}")
    logger.info(f"Allowed origins: {config.allowed_origins}")

    yield

    # Shutdown events
    logger.info("Shutting down Simple AI Chatbot")


# Create FastAPI app
app = FastAPI(
    title="Simple AI Chatbot",
    version="0.1.0",
    description="A simple AI chatbot using FastAPI and WebSocket",
    debug=config.DEBUG,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page."""
    return HTMLResponse(load_cached_template())

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy" if llm_service.is_healthy() else "unhealthy",
        model=llm_service.model_name,
        version="0.1.0"
    )

@app.get("/metrics")
async def metrics():
    """Metrics endpoint for monitoring."""
    return {
        "active_connections": connection_manager.get_connection_count(),
        "model_info": llm_service.get_model_info(),
        "config": {
            "debug": config.DEBUG,
            "model_name": config.MODEL_NAME,
            "host": config.HOST,
            "port": config.PORT
        }
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for chat functionality."""
    await handle_websocket_connection(websocket)


# Make app available for import
__all__ = ["app"]

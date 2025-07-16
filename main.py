import os
import json
import uuid
import logging
from typing import List, Optional
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ValidationError
from langchain_ollama import ChatOllama
import uvicorn


load_dotenv()


class Config:
    DEFAULT_MODEL_NAME: str = os.getenv("DEFAULT_MODEL_NAME", "llama3.1")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    @property
    def allowed_origins(self) -> List[str]:
        if self.DEBUG:
            return ["http://localhost:3000"]
        return os.getenv("ALLOWED_ORIGINS", "").split(",")


class ChatMessage(BaseModel):
    userMsgId: str = Field(..., min_length=1, max_length=50)
    userMsg: str = Field(..., min_length=1, max_length=1000)


class WebSocketResponse(BaseModel):
    status: str
    role: Optional[str] = None
    userMsgId: Optional[str] = None
    userMsg: Optional[str] = None
    assistantMsgId: Optional[str] = None
    assistantMsg: Optional[str] = None


def setup_logging() -> logging.Logger:
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format=log_format,
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


config = Config()
logger = setup_logging()


try:
    llm = ChatOllama(model=config.DEFAULT_MODEL_NAME)
    logger.info(f"Initialized LLM with model: {config.DEFAULT_MODEL_NAME}")
except Exception as e:
    logger.error(f"Failed to initialize LLM: {e}")
    raise


app = FastAPI(
    title="Simple AI chatbot",
    version="0.0.1",
    description="A simple AI chatbot using FastAPI and WebSocket"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.allowed_origins],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

def load_template() -> str:
    """Load HTML template with proper error handling."""
    template_path = Path("static/index.html")
    try:
        with template_path.open("r", encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Template file not found: {template_path}")
        raise HTTPException(status_code=500, detail="Template file not found.")
    except Exception as e:
        logger.error(f"Failed to load template: {e}")
        raise HTTPException(status_code=500, detail="Failed to load template.")


def generate_response_id() -> str:
    """Generate a short response ID."""
    return str(uuid.uuid4())[:8]


async def send_websocket_message(websocket: WebSocket, response: WebSocketResponse) -> None:
    """Send a structured message via WebSocket."""
    try:
        await websocket.send_text(response.model_dump_json(exclude_none=True))
    except Exception as e:
        logger.error(f"Failed to send WebSocket message: {e}")
        raise



@app.get("/")
async def root():
    """Serve the main HTML page."""
    return HTMLResponse(load_template())


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "model": config.DEFAULT_MODEL_NAME}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for chat functionality."""
    await websocket.accept()
    logger.info("WebSocket connection established")
    try:
        while True:
            try:
                raw_message = await websocket.receive_text()
                data = json.loads(raw_message)
                message = ChatMessage(**data)

                response_id = generate_response_id()
                logger.info(f"Processing message {message.userMsgId}: {message.userMsg[:50]}...")

                await send_websocket_message(websocket, WebSocketResponse(
                    status='msg-received',
                    role='user',
                    userMsgId=message.userMsgId,
                    userMsg=message.userMsg,
                ))

                try:
                    for chunks in llm.stream(message.userMsg):
                        await send_websocket_message(websocket, WebSocketResponse(
                            status='response-stream',
                            role='assistant',
                            userMsgId=message.userMsgId,
                            assistantMsgId=response_id,
                            assistantMsg=str(chunks.content),
                        ))
                except Exception as llm_error:
                    logger.error(f"LLM streaming error: {llm_error}")
                    await send_websocket_message(websocket, WebSocketResponse(
                        status='error',
                        role='assistant',
                        userMsgId=message.userMsgId,
                        assistantMsgId=response_id,
                        assistantMsg=f"Error processing your request.",
                    ))

                await send_websocket_message(websocket, WebSocketResponse(
                    status='end',
                    userMsgId=message.userMsgId,
                ))
            except json.JSONDecodeError:
                logger.warning("Received invalid JSON message")
                await send_websocket_message(websocket, WebSocketResponse(
                    status='error',
                    assistantMsg=f"Invalid JSON message received.",
                ))
            except ValidationError as e:
                logger.warning(f"Message validation error: {e}")
                await send_websocket_message(websocket, WebSocketResponse(
                    status='error',
                    assistantMsg=f"Invalid request format.",
                ))
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed by client")
    except Exception as e:
        logger.error(f"Unexpected webSocket error: {e}")
    finally:
        try:
            await websocket.close()
        except:
            pass


if __name__ == "__main__":
    logger.info(f"Starting server on {config.HOST}:{config.PORT}")
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        log_level=config.LOG_LEVEL.lower(),
    )

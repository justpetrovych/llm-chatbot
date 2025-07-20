import json
import uuid
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from ..models import ChatMessage, WebSocketResponse
from ..services.llm_service import llm_service
from ..utils.logging import get_logger
from .manager import connection_manager

logger = get_logger(__name__)


def generate_response_id() -> str:
    """Generate a short response ID."""
    return str(uuid.uuid4())[:8]


async def send_response(websocket: WebSocket, response: WebSocketResponse) -> None:
    """Send a structured response via WebSocket."""
    try:
        await connection_manager.send_message(websocket, response.to_json())
    except Exception as e:
        logger.error(f"Error sending WebSocket response: {e}")
        raise


async def handle_chat_message(websocket: WebSocket, message: ChatMessage) -> None:
    """Handle a chat message from the client."""
    response_id = generate_response_id()

    logger.info(f"Processing message {message.userMsgId}: {message.userMsg[:50]}...")

    # Send acknowledgment
    await send_response(websocket, WebSocketResponse(
        status='msg-received',
        role='assistant',
        userMsgId=message.userMsgId,
        userMsg=None,
        assistantMsgId=response_id,
        assistantMsg=message.userMsg,
    ))

    try:
        # Stream LLM response
        async for chunk in llm_service.stream_response(message.userMsg):
            await send_response(websocket, WebSocketResponse(
                status='response-stream',
                role='assistant',
                userMsgId=message.userMsgId,
                userMsg=None,
                assistantMsgId=response_id,
                assistantMsg=chunk
            ))

    except Exception as e:
        logger.error(f"LLM streaming error: {e}")
        await send_response(websocket, WebSocketResponse(
            status='error',
            role='assistant',
            userMsgId=message.userMsgId,
            userMsg=None,
            assistantMsgId=response_id,
            assistantMsg='Error processing your request. Please try again.'
        ))
        return

    # Send completion signal
    await send_response(websocket, WebSocketResponse(
        status='end',
        role='assistant',
        userMsgId=message.userMsgId,
        userMsg=None,
        assistantMsgId=response_id,
        assistantMsg=None,
    ))


async def handle_websocket_connection(websocket: WebSocket) -> None:
    """Handle a WebSocket connection and its messages."""
    connection_id = await connection_manager.connect(websocket)

    try:
        while True:
            try:
                # Receive and parse a message
                raw_message = await websocket.receive_text()
                data = json.loads(raw_message)
                message = ChatMessage(**data)

                # Handle the chat message
                await handle_chat_message(websocket, message)

            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON from connection {connection_id}")
                await send_response(websocket, WebSocketResponse(
                    status='error',
                    role='assistant',
                    userMsgId=None,
                    userMsg=None,
                    assistantMsgId=None,
                    assistantMsg='Invalid message format: expecting JSON'
                ))

            except ValidationError as e:
                logger.warning(f"Message validation error from {connection_id}: {e}")
                await send_response(websocket, WebSocketResponse(
                    status='error',
                    role='assistant',
                    userMsgId=None,
                    userMsg=None,
                    assistantMsgId=None,
                    assistantMsg='Invalid message format: check required fields'
                ))

            except Exception as e:
                logger.error(
                    f"Unexpected error handling message from {connection_id}: {e}")
                await send_response(websocket, WebSocketResponse(
                    status='error',
                    role='assistant',
                    userMsgId=None,
                    userMsg=None,
                    assistantMsgId=None,
                    assistantMsg='An unexpected error occurred'
                ))

    except WebSocketDisconnect:
        logger.info(f"WebSocket connection {connection_id} disconnected by client")

    except Exception as e:
        logger.error(f"Unexpected WebSocket error for {connection_id}: {e}")

    finally:
        connection_manager.disconnect(websocket)

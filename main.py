from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama import ChatOllama
import logging
import json
import uuid

ALLOWED_ORIGINS = [
    "*",
    "http://localhost:3000/"
]
MODEL_NAME = "llama3.1"

logging.basicConfig(filename='app.log', level=logging.INFO)

llm = ChatOllama(model=MODEL_NAME)

app = FastAPI(title="Simple AI chatbot", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# get template from static/index.html
template = open("static/index.html").read()

@app.get("/")
async def root():
    return HTMLResponse(template)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            req = await websocket.receive_text()
            data = json.loads(req)
            request_id = data['userMsgId']
            user_msg = data['userMsg']
            response_id = str(uuid.uuid4())[:6]
            await websocket.send_text(json.dumps({
                'status': 'msg-received',
                'role': 'user',
                'userMsgId': request_id,
                'userMsg': user_msg,
            }))
            logging.info(f"User Query: {user_msg}")
            for chunks in llm.stream(user_msg):
                await websocket.send_text(json.dumps({
                    'status': 'response-stream',
                    'role': 'assistant',
                    'userMsgId': request_id,
                    'assistantMsgId': response_id,
                    'assistantMsg': str(chunks.content),
                }))
            await websocket.send_text(json.dumps({
                'status': 'end',
                'userMsgId': request_id,
            }))
    except Exception as e:
        error_msg = f'WebSocket error: {str(e)}'
        logging.error(error_msg)
        print(error_msg)
    finally:
        await websocket.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

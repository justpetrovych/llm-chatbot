# Simple AI Chatbot

This project is a simple, full-stack AI chatbot application powered by [FastAPI](https://fastapi.tiangolo.com) on the backend and a modern React frontend. The backend leverages [LangChain](https://www.langchain.com/) to stream responses from an LLM. The frontend provides a clean, responsive chat interface.

---

## Features

- **Real-time Chat**: Communicate with the AI assistant via a WebSocket connection for low-latency, streaming responses.
- **Modern UI**: Responsive React interface with typing indicators and smooth UX.
- **Unique Message IDs**: Each message is tracked with a unique ID for robust client-server communication.
- **CORS Support**: Easily connect from different origins (e.g., local development).
- **Logging**: All user queries are logged for monitoring and debugging.

---
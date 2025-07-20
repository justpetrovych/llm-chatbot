# Simple AI Chatbot

This project is a simple, full-stack AI chatbot application powered by [FastAPI](https://fastapi.tiangolo.com) on the backend and a modern React frontend.  
The backend leverages [LangChain](https://www.langchain.com/) to stream responses from an LLM.  
The frontend provides a clean, responsive chat interface.

---

## Features

- **Real-time Chat**: Communicate with the AI assistant via a WebSocket connection for low-latency, streaming responses.
- **Modern UI**: Responsive React interface with typing indicators and smooth UX.
- **Unique Message IDs**: Each message is tracked with a unique ID for robust client-server communication.
- **CORS Support**: Easily connect from different origins (e.g., local development).
- **Logging**: All user queries are logged for monitoring and debugging.

---

## To Do

- [x] Implement dark/light theme auto-switch based on system settings.
- [x] Enable Markdown in AI/model responses.
- [ ] Enable code formatting in AI/model responses.
- [ ] Add the ability to copy the AI/model response
- [x] Use Pydantic for data validation
- [x] Add loading/error states for network issues.
- [ ] Add support for multiple AI models (model selection dropdown).
- [ ] Add the right side panel with the model settings (temperature, top_p, etc.)
- [ ] Implement the persistent chat history (store messages in a database).
- [ ] Add the left panel with the chat list and button 'new chat'
- [ ] Implement message search functionality within chats.
- [ ] Show model response time and usage statistics.
- [ ] Add voice input and output (speech-to-text and text-to-speech).
- [ ] Add system prompts or context window for better AI guidance.
- [ ] Integrate with external APIs (e.g., Wikipedia, WolframAlpha) for enhanced answers.
- [ ] Provide export chat to PDF/Markdown/CSV.
- [ ] Add an example MCP server and communicate with it (fastMCP)
- [ ] Add an example AI agent and communicate with it (A2A)

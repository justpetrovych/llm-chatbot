import React, { useEffect, useRef, useState } from 'react';
import './App.css';
import TypingIndicator from './components/TypingIndicator';
import { generateShortUniqueId } from './utils';
import Header from './components/Header';
import ChatMessage from './components/ChatMessage';
import InputPanel from './components/InputPanel';

const WS_URL = 'ws://localhost:8000/ws';

interface WSChatMessage {
  role: string;
  userMsgId: string;
  assistantMsgId?: string;
  userMsg?: string;
  assistantMsg?: string;
}

const App = () => {
  const [isDarkTheme, setIsDarkTheme] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [pendingUserMsgId, setPendingUserMsgId] = useState<string | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Theme toggle effect
  useEffect(() => {
    document.body.setAttribute('data-theme', isDarkTheme ? 'dark' : 'light');
  }, [isDarkTheme]);

  // WebSocket setup
  useEffect(() => {
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    setIsDarkTheme(prefersDark);

    const socket = new window.WebSocket(WS_URL);
    setWs(socket);
    socket.onopen = () => setIsConnected(true);
    socket.onclose = () => setIsConnected(false);
    socket.onerror = (e) => console.error('WebSocket error', e);
    return () => socket.close();
  }, []);

  // Scroll to bottom on new message
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, typing]);

  const onExchangeStart = (message: WSChatMessage) => {
    setMessages((prev) => [
      ...prev,
      {
        id: message.userMsgId,
        content: message.userMsg,
        isUser: true,
      },
    ]);
    setTyping(true);
    setPendingUserMsgId(message.userMsgId);
  };

  const onExchangeStream = (message: WSChatMessage) => {
    setTyping(false);
    setMessages((prev) => {
      // If assistantMsgId exists, append content, else add new
      const idx = prev.findIndex((m) => m.id === message.assistantMsgId);
      if (idx !== -1) {
        // Append content
        const updated = [...prev];
        updated[idx] = {
          ...updated[idx],
          content: updated[idx].content + message.assistantMsg,
        };
        return updated;
      } else {
        return [
          ...prev,
          {
            id: message.assistantMsgId,
            content: message.assistantMsg,
            isUser: false,
          },
        ];
      }
    });
  }

  const onExchangeEnd = () => {
    setTyping(false);
    setPendingUserMsgId(null);
  };

  const onExchangeError = () => {
    setTyping(false);
    // Optionally show error
  };

  // WebSocket message handler
  useEffect(() => {
    if (!ws) return;
    ws.onmessage = (event) => {
      const parsed = JSON.parse(event.data);
      switch (parsed.status) {
        case 'msg-received':
          onExchangeStart(parsed);
          break;
        case 'end':
          onExchangeEnd();
          break;
        case 'response-stream':
          onExchangeStream(parsed);
          break;
        case 'error':
          onExchangeError();
          break;
        default:
          // Optionally handle unknown status
          break;
      }
    };
  }, [ws]);

  const handleSend = () => {
    if (!input.trim() || !ws || ws.readyState !== 1) return;
    const message: WSChatMessage = {
      userMsgId: generateShortUniqueId(),
      role: 'user',
      userMsg: input.trim(),
    };
    ws.send(JSON.stringify(message));
    setInput('');
  };

  const handleInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') handleSend();
  };

  return (
    <div className="container">
      <Header
        isConnected={isConnected}
        isDarkTheme={isDarkTheme}
        onToggleTheme={() => setIsDarkTheme((v) => !v)}
      />
      <div className="chat-container" id="chatContainer" ref={chatContainerRef}>
        {messages.map((msg) => (
          <ChatMessage
            key={msg.id}
            id={msg.id}
            content={msg.content}
            isUser={msg.isUser}
          />
        ))}
        {typing && <TypingIndicator />}
      </div>
      <InputPanel
        input={input}
        onInputChange={(e) => setInput(e.target.value)}
        onInputKeyDown={handleInputKeyDown}
        onSend={handleSend}
      />
    </div>
  );
};

export default App;

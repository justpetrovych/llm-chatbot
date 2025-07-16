import React from 'react';
import ReactMarkdown from 'react-markdown';

interface ChatMessageProps {
  id: string;
  content: string;
  isUser: boolean;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ id, content, isUser }) => (
  <div
    className={`message ${isUser ? 'user-message' : 'bot-message'}`}
    id={id}
  >
    <div className="avatar">{isUser ? 'U' : 'AI'}</div>
    <div className="message-bubble">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  </div>
);

export default ChatMessage;

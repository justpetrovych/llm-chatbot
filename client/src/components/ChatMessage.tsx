import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faClipboard, faCheck } from '@fortawesome/free-solid-svg-icons';

interface ChatMessageProps {
  id: string;
  content: string;
  isUser: boolean;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ id, content, isUser }) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
      try {
        await navigator.clipboard.writeText(content);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000); // Reset after 2 seconds
      } catch (err) {
        console.error('Failed to copy text: ', err);
      }
    };

    return (
      <div
        className={`message ${isUser ? 'user-message' : 'bot-message'}`}
        id={id}
      >
        <div className="avatar">{isUser ? 'U' : 'AI'}</div>
        <div className="message-bubble">
          <ReactMarkdown>{content}</ReactMarkdown>
          <button
            className="copy-button"
            onClick={handleCopy}
            title="Copy message to clipboard"
            aria-label="Copy message to clipboard"
          >
            <FontAwesomeIcon inverse icon={copied ? faCheck : faClipboard } />
          </button>

        </div>
      </div>
    );
  };

export default ChatMessage;

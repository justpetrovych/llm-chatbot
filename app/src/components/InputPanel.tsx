import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

interface InputPanelProps {
  input: string;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onInputKeyDown: (e: React.KeyboardEvent<HTMLInputElement>) => void;
  onSend: () => void;
}

const InputPanel: React.FC<InputPanelProps> = ({ input, onInputChange, onInputKeyDown, onSend }) => (
  <div className="input-container">
    <div className="input-wrapper">
      <input
        type="text"
        className="message-input"
        placeholder="Type your message..."
        aria-label="Message input"
        value={input}
        onChange={onInputChange}
        onKeyDown={onInputKeyDown}
        autoFocus
      />
      <div className="action-buttons">
        <button className="send-button" onClick={onSend}>
          <span>Send</span>
          <FontAwesomeIcon icon={faPaperPlane} />
        </button>
      </div>
    </div>
  </div>
);

export default InputPanel;

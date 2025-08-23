import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMoon, faSun } from '@fortawesome/free-solid-svg-icons';

interface HeaderProps {
  isConnected: boolean;
  isDarkTheme: boolean;
  label: string;
  onToggleTheme: () => void;
  models: string[];
  selectedModel: string;
  setSelectedModel: (model: string) => void;
  modelSelectDisabled: boolean;
}

const Header: React.FC<HeaderProps> = ({ isConnected, isDarkTheme, label, onToggleTheme, models, selectedModel, setSelectedModel, modelSelectDisabled }) => (
  <header className="header">
    <div className="header-title">
      <h1>{ label }</h1>
      <div className="bot-status">
        <div className={`status-indicator ${isConnected ? 'online' : 'offline'}`} />
        <span>{isConnected ? 'Online' : 'Offline'}</span>
        <label htmlFor="model-select" style={{ marginLeft: 16, marginRight: 8 }}>Model:</label>
        <select
          id="model-select"
          value={selectedModel}
          onChange={e => setSelectedModel(e.target.value)}
          disabled={modelSelectDisabled}
          style={{ marginRight: 8 }}
        >
          {models.map(m => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>
      </div>
    </div>
    <div className="controls">
      <button
        className="theme-toggle"
        aria-label="Toggle theme"
        onClick={onToggleTheme}
      >
        <FontAwesomeIcon icon={isDarkTheme ? faSun : faMoon} />
      </button>
    </div>
  </header>
);

export default Header;

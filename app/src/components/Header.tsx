import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMoon, faSun } from '@fortawesome/free-solid-svg-icons';

interface HeaderProps {
  isConnected: boolean;
  isDarkTheme: boolean;
  label: string;
  onToggleTheme: () => void;
}

const Header: React.FC<HeaderProps> = ({ isConnected, isDarkTheme, label, onToggleTheme }) => (
  <header className="header">
    <div className="header-title">
      <h1>{ label }</h1>
      <div className="bot-status">
        <div className={`status-indicator ${isConnected ? 'online' : 'offline'}`} />
        <span>{isConnected ? 'Online' : 'Offline'}</span>
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

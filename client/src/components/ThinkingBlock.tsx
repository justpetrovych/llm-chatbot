import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronDown, faChevronRight, faBrain } from '@fortawesome/free-solid-svg-icons';

interface ThinkingBlockData {
  content: string;
  position: number;
}

interface ThinkingBlockProps {
  thinkingBlocks: ThinkingBlockData[];
}

const ThinkingBlock: React.FC<ThinkingBlockProps> = ({ thinkingBlocks }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!thinkingBlocks || thinkingBlocks.length === 0) {
    return null;
  }

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="thinking-blocks">
      <button
        className="thinking-toggle"
        onClick={toggleExpanded}
        title={isExpanded ? 'Hide thinking process' : 'Show thinking process'}
        aria-label={isExpanded ? 'Hide thinking process' : 'Show thinking process'}
      >
        <FontAwesomeIcon 
          icon={faBrain} 
          className="thinking-icon"
        />
        <span className="thinking-label">AI Thinking</span>
        <FontAwesomeIcon 
          icon={isExpanded ? faChevronDown : faChevronRight} 
          className="thinking-chevron"
        />
      </button>
      
      {isExpanded && (
        <div className="thinking-content">
          {thinkingBlocks.map((block, index) => (
            <div key={index} className="thinking-block">
              <div className="thinking-block-content">
                {block.content}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ThinkingBlock;
"""Utility for parsing and handling AI thinking blocks."""

import re
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class ThinkingBlock:
    """Represents a thinking block with its content."""
    content: str
    position: int  # Position in the original text


@dataclass
class ParsedMessage:
    """Represents a message with separated thinking blocks and main content."""
    main_content: str
    thinking_blocks: List[ThinkingBlock]
    has_thinking: bool


def parse_thinking_blocks(text: str) -> ParsedMessage:
    """
    Parse thinking blocks from text content.
    
    Args:
        text: The text content that may contain <think> tags
        
    Returns:
        ParsedMessage with separated thinking blocks and main content
    """
    if not text:
        return ParsedMessage(
            main_content="",
            thinking_blocks=[],
            has_thinking=False
        )
    
    # Pattern to match thinking blocks with case-insensitive tags
    pattern = re.compile(r'<think(?:\s[^>]*)?>(.+?)</think>', re.DOTALL | re.IGNORECASE)
    
    thinking_blocks = []
    matches = pattern.finditer(text)
    
    for i, match in enumerate(matches):
        thinking_blocks.append(ThinkingBlock(
            content=match.group(1).strip(),
            position=i
        ))
    
    # Remove thinking blocks from main content
    main_content = pattern.sub('', text).strip()
    
    # Clean up multiple newlines and spaces
    main_content = re.sub(r'\n\s*\n\s*\n', '\n\n', main_content)
    main_content = main_content.strip()
    
    return ParsedMessage(
        main_content=main_content,
        thinking_blocks=thinking_blocks,
        has_thinking=len(thinking_blocks) > 0
    )


def format_message_with_thinking(parsed: ParsedMessage) -> Dict[str, Any]:
    """
    Format a parsed message for API response.
    
    Args:
        parsed: ParsedMessage object
        
    Returns:
        Dictionary with formatted message data
    """
    return {
        "content": parsed.main_content,
        "has_thinking": parsed.has_thinking,
        "thinking_blocks": [
            {
                "content": block.content,
                "position": block.position
            }
            for block in parsed.thinking_blocks
        ] if parsed.has_thinking else []
    }
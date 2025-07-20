"""Template loading utilities."""

from pathlib import Path
from fastapi import HTTPException
from .logging import get_logger

logger = get_logger(__name__)


def load_template(template_path: str = "static/index.html") -> str:
    """Load HTML template with proper error handling."""

    template_file = Path(template_path)

    try:
        with template_file.open('r', encoding='utf-8') as f:
            content = f.read()
            logger.info(f"Template loaded successfully: {template_path}")
            return content

    except FileNotFoundError:
        error_msg = f"Template file not found: {template_path}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail="Template file not found")

    except Exception as e:
        error_msg = f"Error loading template {template_path}: {e}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail="Error loading template")


def get_template_cache():
    """Simple template caching mechanism."""
    _cache = {}

    def cached_load_template(template_path: str = "static/index.html") -> str:
        if template_path not in _cache:
            _cache[template_path] = load_template(template_path)
        return _cache[template_path]

    return cached_load_template


# Create a cached template loader
load_cached_template = get_template_cache()

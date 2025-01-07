"""
fast-html2md
Convert HTML to Markdown for LLM input extraction.
"""

from .converter import HTMLToMarkdown
from .exceptions import ConversionError

__version__ = "0.1.0"
__all__ = ["HTMLToMarkdown", "ConversionError"]

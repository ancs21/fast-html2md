import tiktoken
from typing import Optional
from .cleaners import HTMLCleanerPipeline
from .models import MODEL_INFO
from .exceptions import ConversionError


class HTMLToMarkdown:
    """Main converter class for HTML to Markdown conversion."""

    def __init__(self, config: Optional[dict] = None):
        """Initialize the converter with optional configuration.

        Args:
            config: Optional configuration dictionary with supported keys:
                - model_info: ModelInfo instance for token counting and pricing
                - extract_body: Whether to extract content from body tag only (default: True)
                - remove_attributes: Whether to remove HTML attributes (default: True)
                - replace_classes: Whether to replace class attributes (default: True)
                - replace_ids: Whether to replace id attributes (default: True)
                - minify: Whether to minify HTML (default: True)
                - trim_a_tags: Whether to trim anchor tags (default: True)
                - convert_markdown: Whether to convert to markdown (default: True)
        """
        self._init_config(config)
        self._init_cleaner()

    def _init_config(self, config: Optional[dict]) -> None:
        """Initialize configuration settings.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.model_info = self.config.get("model_info", MODEL_INFO)
        self.extract_body = self.config.get("extract_body", True)
        self.remove_attributes = self.config.get("remove_attributes", True)
        self.replace_classes = self.config.get("replace_classes", True)
        self.replace_ids = self.config.get("replace_ids", True)
        self.minify = self.config.get("minify", True)
        self.trim_a_tags = self.config.get("trim_a_tags", True)
        self.convert_markdown = self.config.get("convert_markdown", True)

    def _init_cleaner(self) -> None:
        """Initialize the HTML cleaner pipeline with current settings."""
        self.cleaner = HTMLCleanerPipeline(
            model=self.model_info.name,
            price_per_million_tokens=self.model_info.price_per_million_tokens,
            extract_body=self.extract_body,
            remove_attributes=self.remove_attributes,
            replace_classes=self.replace_classes,
            replace_ids=self.replace_ids,
            minify=self.minify,
            trim_a_tags=self.trim_a_tags,
            convert_markdown=self.convert_markdown,
        )

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in the text.

        Args:
            text: Input text to count tokens for

        Returns:
            Number of tokens in the text
        """
        encoding = tiktoken.encoding_for_model(self.model_info.name)
        return len(encoding.encode(text))

    def compute_cost(self, token_count: int) -> float:
        """Compute the cost for the given number of tokens.

        Args:
            token_count: Number of tokens to compute cost for

        Returns:
            Computed cost in currency units
        """
        return (token_count / 1_000_000) * self.model_info.price_per_million_tokens

    def convert(self, html: str) -> str:
        """Convert HTML string to Markdown.

        Args:
            html: Input HTML string

        Returns:
            Converted Markdown string

        Raises:
            ConversionError: If conversion fails
        """

        if html is None:
            raise ConversionError("HTML content cannot be None")

        if not isinstance(html, str):
            raise ConversionError("HTML content must be a string")

        if not html.strip():
            raise ConversionError("HTML content cannot be empty")

        try:
            result = self.cleaner.clean(html)

            if not result or not result.strip():
                raise ConversionError("Conversion resulted in empty output")

            return result

        except Exception as e:
            raise ConversionError(f"Failed to convert HTML: {str(e)}")

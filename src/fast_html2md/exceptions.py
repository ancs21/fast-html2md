class ConversionError(Exception):
    """Base exception for HTML to Markdown conversion errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

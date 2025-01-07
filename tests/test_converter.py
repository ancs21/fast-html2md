import pytest
from src.fast_html2md.converter import HTMLToMarkdown
from src.fast_html2md.models import Models, ModelInfo
from src.fast_html2md.exceptions import ConversionError


def test_converter_initialization():
    # Test default initialization
    converter = HTMLToMarkdown()
    assert converter.model_info == Models.GPT4O_MINI
    assert converter.extract_body is True

    # Test custom initialization
    custom_model = ModelInfo("custom-model", 1.0)
    converter = HTMLToMarkdown(
        config={
            "model_info": custom_model,
            "extract_body": False,
            "remove_attributes": False,
            "replace_classes": False,
            "replace_ids": False,
            "minify": False,
            "trim_a_tags": False,
            "convert_markdown": False,
        }
    )
    assert converter.model_info == custom_model
    assert converter.extract_body is False


def test_converter_token_counting():
    converter = HTMLToMarkdown()
    text = "Hello, world!"
    token_count = converter.count_tokens(text)
    assert token_count > 0

    # Test cost computation
    cost = converter.compute_cost(token_count)
    assert (
        cost
        == (token_count / 1_000_000) * converter.model_info.price_per_million_tokens
    )


def test_converter_error_handling():
    converter = HTMLToMarkdown()

    # Test None input
    with pytest.raises(ConversionError) as exc_info:
        converter.convert(None)
    assert "HTML content cannot be None" in str(exc_info.value)

    # Test empty input
    with pytest.raises(ConversionError) as exc_info:
        converter.convert("")
    assert "HTML content cannot be empty" in str(exc_info.value)

    # Test non-string input
    with pytest.raises(ConversionError) as exc_info:
        converter.convert(123)
    assert "HTML content must be a string" in str(exc_info.value)

    # Test conversion that results in empty output
    with pytest.raises(ConversionError) as exc_info:
        converter.convert("<!-- just a comment -->")
    assert "Conversion resulted in empty output" in str(exc_info.value)


def test_converter_basic_conversion():
    converter = HTMLToMarkdown()

    # Test basic HTML to Markdown conversion
    html = "<h1>Hello</h1><p>This is a test</p>"
    result = converter.convert(html)
    assert result.strip() == "Hello\n=====\n\nThis is a test"

    # Test conversion with links
    html = '<p>Check out <a href="https://example.com">this link</a></p>'
    result = converter.convert(html)
    assert result.strip() == "Check out this link"

    # Test conversion with formatting
    html = "<p><strong>Bold</strong> and <em>italic</em> text</p>"
    result = converter.convert(html)
    assert result.strip() == "**Bold** and *italic* text"


def test_converter_reinit():
    converter = HTMLToMarkdown()

    # Test reinitializing with new config
    new_config = {
        "model_info": Models.GPT4O,
        "extract_body": False,
    }
    converter._init_config(new_config)
    converter._init_cleaner()

    assert converter.model_info == Models.GPT4O
    assert converter.extract_body is False

    # Verify cleaner is properly reinitialized
    assert converter.cleaner.model == Models.GPT4O.name
    assert (
        converter.cleaner.price_per_million_tokens
        == Models.GPT4O.price_per_million_tokens
    )
    assert converter.cleaner.extract_body is False

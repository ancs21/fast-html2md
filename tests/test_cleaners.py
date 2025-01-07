from src.fast_html2md.cleaners import HTMLCleanerPipeline
from src.fast_html2md.models import ModelInfo


def test_html_cleaner_pipeline():
    # Reference the test HTML file
    with open("test.html", "r", encoding="utf-8") as f:
        test_html = f.read()

    # Initialize pipeline with all cleaning options enabled
    pipeline = HTMLCleanerPipeline(
        model="gpt-4",
        price_per_million_tokens=10.0,
        extract_body=True,
        remove_attributes=True,
        replace_classes=True,
        replace_ids=True,
        minify=True,
        trim_a_tags=True,
        convert_markdown=True,
    )

    # Test token counting
    initial_tokens = pipeline.count_tokens(test_html)
    assert initial_tokens > 0

    # Test cost computation
    cost = pipeline.compute_cost(initial_tokens)
    assert cost == (initial_tokens / 1_000_000) * 10.0

    # Test body extraction
    body_content = pipeline.extract_body_content(test_html)
    assert "<body" in body_content
    assert len(body_content) < len(test_html)

    # Test attribute removal
    cleaned_html = pipeline.remove_html_attributes(test_html)
    assert 'content="IE=Edge"' not in cleaned_html
    assert "class=" in cleaned_html  # Should keep class attributes
    assert "id=" in cleaned_html  # Should keep id attributes

    # Test class name replacement
    replaced_classes = pipeline.replace_class_names(test_html)
    assert 'class="devsite-nav-item"' not in replaced_classes
    # Look for any numbered class pattern instead of specific "1"
    assert any(f'class="{i}"' in replaced_classes for i in range(1, 100))

    # Test ID replacement
    replaced_ids = pipeline.replace_id_names(test_html)
    assert 'id="1"' in replaced_ids
    assert 'id="devsite-hamburger-menu"' not in replaced_ids

    # Test minification
    minified = pipeline.minify_html(test_html)
    assert len(minified) < len(test_html)
    assert "  " not in minified  # No double spaces
    assert "\n" not in minified  # No newlines

    # Test a tag trimming
    trimmed = pipeline.trim_a_tags_and_unwrap(test_html)
    assert len(trimmed) <= len(test_html)

    # Test markdown conversion
    markdown = pipeline.convert_to_markdown(test_html)
    assert "<html" not in markdown
    assert "<body" not in markdown

    # Test full pipeline
    final_result = pipeline.clean(test_html)
    assert len(final_result) < len(test_html)

    # Test model info update
    new_model_info = ModelInfo(name="gpt-3.5-turbo", price_per_million_tokens=5.0)
    pipeline.set_model_info(new_model_info)
    assert pipeline.model == "gpt-3.5-turbo"
    assert pipeline.price_per_million_tokens == 5.0

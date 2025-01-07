# fast-html2md

Convert HTML to Markdown for LLM input extraction.

## Installation

```bash

# use pip
pip install fast-html2md

# or use poetry
poetry add fast-html2md

# or use uv
uv add fast-html2md
```

## Usage

```python
from fast_html2md import HTMLToMarkdown

converter = HTMLToMarkdown()

html = """
<!DOCTYPE html>
<html>
<body>
  <h1 id="title" data-updated="20201101">Hi there</h1>
  <div class="post">
    Lorem Ipsum is simply dummy text of the printing and typesetting industry.
  </div>
  <div class="post">
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
  </div>
</body>
</html>
"""

markdown = converter.convert(html)

print(markdown)

# Count tokens
token_count = converter.count_tokens(markdown)
print(f"Token count: {token_count}")

# Compute cost
cost = converter.compute_cost(token_count)
print(f"Estimated cost: ${cost:.6f}")
```

## Features

- Fast HTML to Markdown conversion
- Optimized for LLM input processing
- Built-in token counting using tiktoken
- Clean and minimal output

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/ancs21/fast-html2md/blob/main/LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

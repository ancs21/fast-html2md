# fast-html2md [![PyPI version](https://badge.fury.io/py/fast-html2md.svg)](https://badge.fury.io/py/fast-html2md) [![Run Tests](https://github.com/ancs21/fast-html2md/actions/workflows/test.yml/badge.svg)](https://github.com/ancs21/fast-html2md/actions/workflows/test.yml) [![codecov](https://codecov.io/github/ancs21/fast-html2md/branch/main/graph/badge.svg?token=8KP9MXS92V)](https://codecov.io/github/ancs21/fast-html2md)

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

## Examples

- [GitHub Trending](examples/github-trending.py)

```
# Prerequisites
# ----
# This script is used to scrape the GitHub Trending page and extract the data into a JSON object.
# !uv pip install fast-html2md hrequests google-genai python-dotenv
# create .env file with GOOGLE_API_KEY=your_api_key
# uv run python examples/github-trending.py
# ----

# Run the script
uv run python examples/github-trending.py

# Result (JSON / 10 Jan 2025)
{
  "repositories": [
    {
      "description": "Your AI second brain. Self-hostable. Get answers from the web or your docs. Build custom agents, schedule automations, do deep research. Turn any online or local LLM into your personal, autonomous AI (gpt, claude, gemini, llama, qwen, mistral). Get started - free.",
      "forks": 1214,
      "href": "khoj-ai /  khoj",
      "name": "khoj",
      "owner": "khoj-ai",
      "rank": 1,
      "repository_name": "khoj-ai /  khoj",
      "stars": 23173,
     "built_by": [],
      "language": "Python",
      "todays_stars": 1508
    },
    {
      "description": "Resume Matcher is an open source, free tool to improve your resume. It works by using AI, Reader LLMs, to compare and rank resumes with job descriptions.",
      "forks": 2528,
      "href": "srbhr /  Resume-Matcher",
      "name": "Resume-Matcher",
      "owner": "srbhr",
      "rank": 2,
      "repository_name": "srbhr /  Resume-Matcher",
      "stars": 6814,
    "built_by": [],
      "language": "Python",
      "todays_stars": 436
    },
    {
       "description": "How to run an Ink Node",
      "forks": 232,
      "href": "inkonchain /  node",
      "name": "node",
      "owner": "inkonchain",
      "rank": 3,
      "repository_name": "inkonchain /  node",
      "stars": 17265,
     "built_by": [],
     "language": "Shell",
      "todays_stars": 3303
    },
    {
     "description": "VILA is a family of state-of-the-art vision language models (VLMs) for diverse multimodal AI tasks across the edge, data center, and cloud.",
      "forks": 198,
      "href": "NVlabs /  VILA",
       "name": "VILA",
      "owner": "NVlabs",
      "rank": 4,
      "repository_name": "NVlabs /  VILA",
      "stars": 2498,
    "built_by": [],
      "language": "Python",
      "todays_stars": 60
    },
    {
      "description": "🚀🤖 Crawl4AI: Open-source LLM Friendly Web Crawler & Scraper",
      "forks": 1691,
      "href": "unclecode /  crawl4ai",
      "name": "crawl4ai",
      "owner": "unclecode",
      "rank": 5,
      "repository_name": "unclecode /  crawl4ai",
      "stars": 23533,
    "built_by": [],
      "language": "Python",
      "todays_stars": 1106
    },
    {
      "description": "Ink Documentation",
      "forks": 172,
      "href": "inkonchain /  docs",
       "name": "docs",
      "owner": "inkonchain",
      "rank": 6,
      "repository_name": "inkonchain /  docs",
      "stars": 17200,
     "built_by": [],
     "language": "MDX",
      "todays_stars": 3301
    },
    {
     "description": "GoogleTest - Google Testing and Mocking Framework",
      "forks": 10223,
      "href": "google /  googletest",
       "name": "googletest",
      "owner": "google",
      "rank": 7,
      "repository_name": "google /  googletest",
      "stars": 35180,
    "built_by": [],
      "language": "C++",
      "todays_stars": 10
    },
        {
      "description": "Build your own AI friend",
       "forks": 338,
      "href": "78 /  xiaozhi-esp32",
      "name": "xiaozhi-esp32",
      "owner": "78",
      "rank": 8,
      "repository_name": "78 /  xiaozhi-esp32",
      "stars": 1973,
     "built_by": [],
     "language": "C",
      "todays_stars": 437
    },
    {
     "description": "Firebase SDK for Apple App Development",
      "forks": 1504,
      "href": "firebase /  firebase-ios-sdk",
      "name": "firebase-ios-sdk",
      "owner": "firebase",
      "rank": 9,
      "repository_name": "firebase /  firebase-ios-sdk",
      "stars": 5820,
    "built_by": [],
      "language": "C++",
      "todays_stars": 38
    },
    {
     "description": "PyTorch native post-training library",
      "forks": 476,
      "href": "pytorch /  torchtune",
      "name": "torchtune",
       "owner": "pytorch",
       "rank": 10,
      "repository_name": "pytorch /  torchtune",
      "stars": 4601,
     "built_by": [],
      "language": "Python",
      "todays_stars": 8
    },
    {
       "description": "Fast C++ logging library.",
      "forks": 4636,
      "href": "gabime /  spdlog",
      "name": "spdlog",
      "owner": "gabime",
      "rank": 11,
      "repository_name": "gabime /  spdlog",
      "stars": 24964,
   "built_by": [],
      "language": "C++",
      "todays_stars": 15
    },
    {
      "description": "Apache Thrift",
      "forks": 4037,
      "href": "apache /  thrift",
       "name": "thrift",
      "owner": "apache",
      "rank": 12,
      "repository_name": "apache /  thrift",
      "stars": 10508,
    "built_by": [],
      "language": "C++",
      "todays_stars": 12
    },
    {
      "description": "Autonomous coding agent right in your IDE, capable of creating/editing files, executing commands, using the browser, and more with your permission every step of the way.",
      "forks": 1762,
      "href": "cline /  cline",
      "name": "cline",
       "owner": "cline",
      "rank": 13,
      "repository_name": "cline /  cline",
      "stars": 20784,
    "built_by": [],
      "language": "TypeScript",
      "todays_stars": 345
    },
    {
      "description": "A BNB Smart Chain client based on the go-ethereum fork",
      "forks": 1587,
      "href": "bnb-chain /  bsc",
      "name": "bsc",
       "owner": "bnb-chain",
      "rank": 14,
      "repository_name": "bnb-chain /  bsc",
      "stars": 2833,
   "built_by": [],
      "language": "Go",
      "todays_stars": 13
    }
  ]
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/ancs21/fast-html2md/blob/main/LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

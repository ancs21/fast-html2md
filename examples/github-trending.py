# ----
# This script is used to scrape the GitHub Trending page and extract the data into a JSON object.
# !uv pip install fast-html2md hrequests google-genai python-dotenv
# create .env file with GOOGLE_API_KEY=your_api_key
# uv run python examples/github-trending.py
# ----

import os
import hrequests
from fast_html2md import HTMLToMarkdown
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def main():
    url = "https://github.com/trending"
    response = hrequests.get(url)
    html = response.text
    converter = HTMLToMarkdown()
    markdown = converter.convert(html)
    # print(markdown)
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=f"""
    Extract the following Markdown into a JSON object:
    {markdown}
    """,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "repositories": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "rank": {"type": "integer"},
                                "name": {"type": "string"},
                                "owner": {"type": "string"},
                                "repository_name": {"type": "string"},
                                "description": {"type": "string"},
                                "language": {"type": "string"},
                                "stars": {"type": "integer"},
                                "forks": {"type": "integer"},
                                "todays_stars": {"type": "number"},
                                "built_by": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "username": {"type": "string"},
                                            "avatar_url": {"type": "string"},
                                            "href": {"type": "string"},
                                        },
                                        "required": ["username", "href"],
                                    },
                                },
                                "href": {"type": "string"},
                            },
                            "required": [
                                "rank",
                                "name",
                                "owner",
                                "repository_name",
                                "description",
                                "stars",
                                "forks",
                                "href",
                            ],
                        },
                    },
                },
                "required": ["repositories"],
                "description": "Schema for the JSON output of scraping GitHub Trending page.",
            },
        ),
    )
    print(response.text)


if __name__ == "__main__":
    main()

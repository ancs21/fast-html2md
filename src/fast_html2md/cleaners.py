import re
import tiktoken
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from functools import lru_cache

from src.fast_html2md.models import ModelInfo


class HTMLCleanerPipeline:
    def __init__(
        self,
        *,
        model: str,
        price_per_million_tokens: float,
        extract_body: bool = False,
        remove_attributes: bool = False,
        replace_classes: bool = False,
        replace_ids: bool = False,
        minify: bool = False,
        trim_a_tags: bool = False,
        convert_markdown: bool = False,
    ):
        self.model = model
        self.price_per_million_tokens = price_per_million_tokens
        self.extract_body = extract_body
        self.remove_attributes = remove_attributes
        self.replace_classes = replace_classes
        self.replace_ids = replace_ids
        self.minify = minify
        self.trim_a_tags = trim_a_tags
        self.convert_markdown = convert_markdown
        self.class_counter = 0
        self.id_counter = 0

    def count_tokens(self, text: str) -> int:
        encoding = tiktoken.encoding_for_model(self.model)
        return len(encoding.encode(text))

    def compute_cost(self, token_count: int) -> float:
        return (token_count / 1_000_000) * self.price_per_million_tokens

    @lru_cache(maxsize=128)
    def _parse_html(self, html_content: str) -> BeautifulSoup:
        return BeautifulSoup(html_content, "html.parser")

    def extract_body_content(self, html_content: str) -> str:
        soup = self._parse_html(html_content)
        body = soup.find("body")
        return str(body) if body else html_content

    def remove_html_attributes(self, html_content: str) -> str:
        soup = self._parse_html(html_content)
        for script in soup(["script", "style"]):
            script.decompose()
        attrs_to_keep = ["class", "id", "data-testid"]
        for tag in soup.find_all():
            for attr in list(tag.attrs.keys()):
                if attr not in attrs_to_keep:
                    del tag[attr]
        return str(soup)

    def replace_class_names(self, html_content: str) -> str:
        soup = self._parse_html(html_content)
        classes = set()
        for tag in soup.find_all(class_=True):
            classes.update(tag.get("class", []))

        mapping = {}
        for class_name in sorted(classes):
            self.class_counter += 1
            mapping[class_name] = str(self.class_counter)

        for tag in soup.find_all(class_=True):
            original_classes = tag.get("class", [])
            new_classes = [mapping.get(cls, cls) for cls in original_classes]
            tag["class"] = new_classes

        return str(soup)

    def replace_id_names(self, html_content: str) -> str:
        soup = self._parse_html(html_content)
        ids = set()
        for tag in soup.find_all(id=True):
            ids.add(tag.get("id"))

        mapping = {}
        for id_name in sorted(ids):
            self.id_counter += 1
            mapping[id_name] = str(self.id_counter)

        for tag in soup.find_all(id=True):
            original_id = tag.get("id")
            new_id = mapping.get(original_id, original_id)
            tag["id"] = new_id

        return str(soup)

    def minify_html(self, html_content: str) -> str:
        html_content = re.sub(r"<!--.*?-->", "", html_content, flags=re.DOTALL)
        html_content = re.sub(r">\s+<", "><", html_content)
        html_content = html_content.strip()
        html_content = re.sub(r"\s+", " ", html_content)
        return html_content

    def trim_a_tags_and_unwrap(self, html_content: str) -> str:
        soup = self._parse_html(html_content)
        for a_tag in soup.find_all("a"):
            if not a_tag.attrs:
                a_tag.unwrap()
        return str(soup)

    def convert_to_markdown(self, html_content: str) -> str:
        return md(html_content)

    def clean(self, html_content: str) -> str:
        if self.extract_body:
            html_content = self.extract_body_content(html_content)

        if self.remove_attributes:
            html_content = self.remove_html_attributes(html_content)

        if self.replace_classes:
            html_content = self.replace_class_names(html_content)

        if self.replace_ids:
            html_content = self.replace_id_names(html_content)

        if self.minify:
            html_content = self.minify_html(html_content)

        if self.trim_a_tags:
            html_content = self.trim_a_tags_and_unwrap(html_content)

        if self.convert_markdown:
            html_content = self.convert_to_markdown(html_content)

        return html_content

    def set_model_info(self, model_info: ModelInfo):
        self.model = model_info.name
        self.price_per_million_tokens = model_info.price_per_million_tokens

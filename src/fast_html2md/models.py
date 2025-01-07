from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class ModelInfo:
    name: str
    price_per_million_tokens: float


class Models:
    GPT4O_MINI: Final[ModelInfo] = ModelInfo("gpt-4o-mini", 0.150)
    GPT4O: Final[ModelInfo] = ModelInfo("gpt-4o", 5.0)


MODEL_INFO: Final[ModelInfo] = Models.GPT4O_MINI

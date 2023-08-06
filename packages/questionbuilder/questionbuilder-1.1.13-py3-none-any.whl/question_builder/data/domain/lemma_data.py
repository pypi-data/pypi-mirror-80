import typing as t
from dataclasses import dataclass

from .data_question import DataQuestion


@dataclass
class LemmaData:
    data_question: DataQuestion
    level: int = 1
    mastered: bool = False

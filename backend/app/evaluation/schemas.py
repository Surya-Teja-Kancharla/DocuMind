from dataclasses import dataclass
from typing import List


@dataclass
class EvaluationSample:
    question: str
    answer: str
    contexts: List[str]

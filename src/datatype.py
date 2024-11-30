from dataclasses import dataclass
from enum import Enum


@dataclass
class Vote:
    session_id: str
    candidate: int
    voter_id: int

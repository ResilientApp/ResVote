from dataclasses import dataclass, field
from typing import Any, Dict
from datetime import datetime


@dataclass
class Vote:
    election_id: str
    candidate_name: str
    voter_id: str

    # transfer datetime to json format
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    @property
    def transaction_id(self):
        return f"{self.election_id}++{self.voter_id}"


@dataclass
class Voter:
    voter_id: str
    password: str

    age: int = 20
    gender: str = "male"
    region: str = "unknown"
    race: str = "unknown"
    education: str = "unknown"

    @property
    def transaction_id(self) -> str:
        return self.voter_id

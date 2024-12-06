from dataclasses import dataclass, field
from typing import Any, Dict
from datetime import datetime


@dataclass
class Vote:
    election_id: str
    candidate_name: str
    voter_id: str
    attributes: Dict[str, str] = field(default_factory=dict)
    #transfer datetime to json format
    timestamp: datetime = field(default_factory=lambda:datetime.utcnow().isoformat())
    
    @property
    def transaction_id(self):
        return f"{self.election_id}++{self.voter_id}"

@dataclass
class Voter:
    voter_id: str
    age: int
    gender: str
    region: str
    race: str
    education: str

    @property
    def transaction_id(self) -> str:
        return self.voter_id



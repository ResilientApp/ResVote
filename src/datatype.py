from dataclasses import dataclass


@dataclass
class Vote:
    election_id: str
    candidate_name: str
    voter_id: str
    
    @property
    def transaction_id(self):
        return f"{self.election_id}++{self.voter_id}"



from dataclasses import dataclass


@dataclass
class Vote:
    session_id: str
    candidate: str
    voter_id: str
    
    @property
    def key(self):
        return f"{self.session_id}++{self.voter_id}"



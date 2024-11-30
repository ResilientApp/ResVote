from dataclasses import dataclass
from enum import Enum
from hypothesis import given
from hypothesis.strategies import SearchStrategy, composite, sampled_from, text
from typing import Callable

@dataclass
class Vote:
    session_id: str
    candidate: str
    voter_id: str
    
    @property
    def key(self):
        return f"{self.session_id}++{self.voter_id}"


@composite
def vote_gen(draw: Callable[[SearchStrategy], str]) -> Vote:
    session_ids = ["test_vote_1", "test_vote_2", "test_vote_3"]
    candidates = ["Alice", "Bob", "Charlie"]
    
    session_id = draw(sampled_from(session_ids))
    candidate = draw(sampled_from(candidates))
    voter_id = draw(text(min_size=1, max_size=10)) 
    return Vote(session_id=session_id, candidate=candidate, voter_id=voter_id)

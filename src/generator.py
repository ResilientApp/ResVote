from hypothesis.strategies import SearchStrategy, composite, sampled_from, text, lists
from typing import Callable
import string

from .datatype import Vote


@composite
def vote_gen(draw: Callable[[SearchStrategy], str]) -> Vote:
    session_ids = ["test_vote_1", "test_vote_2", "test_vote_3"]
    candidates = ["Alice", "Bob", "Charlie"]
    
    session_id = draw(sampled_from(session_ids))
    candidate = draw(sampled_from(candidates))
    voter_id = draw(text(min_size=1, max_size=10, alphabet=string.ascii_letters)) 
    return Vote(session_id=session_id, candidate=candidate, voter_id=voter_id)

vote_list_gen = lists(vote_gen(), min_size=1, max_size=10)
from hypothesis.strategies import SearchStrategy, composite, sampled_from, text, lists
from typing import Callable
import string

from .datatype import Vote


@composite
def vote_gen(draw: Callable[[SearchStrategy], str]) -> Vote:
    election_ids = ["test_vote_1", "test_vote_2", "test_vote_3"]
    candidate_names = ["Alice", "Bob", "Charlie"]
    
    election_id = draw(sampled_from(election_ids))
    candidate_name = draw(sampled_from(candidate_names))
    voter_id = draw(text(min_size=1, max_size=10, alphabet=string.ascii_letters)) 
    return Vote(election_id=election_id, candidate_name=candidate_name, voter_id=voter_id)

vote_list_gen = lists(vote_gen(), min_size=50, max_size=100)
"""! NOTE: this test does not work due to the db graph ql cannot handle request at this rate
"""

from hypothesis import given, settings
from hypothesis.strategies import lists
from src.datatype import Vote
from src.vote_server import VoteServer
from src.generator import vote_list_gen

@settings(deadline=None, max_examples=3)
@given(votes=vote_list_gen)
def test_one_vote_per_voter_per_session(votes: list[Vote]):
    server = VoteServer("config.yaml", None)
    _ = server.create_all(votes)
    all_votes = server.read_all()
    
    session_data_dict: dict[str, set[dict]] = {}
    
    for v in all_votes:
        if v.election_id not in session_data_dict:
            session_data_dict[v.election_id] = set()
        data = {
            "candidate_name": v.candidate_name,
            "voter_id": v.voter_id
        }
        assert data not in session_data_dict[v.election_id]
        session_data_dict[v.election_id].add(data)
    

test_one_vote_per_voter_per_session()
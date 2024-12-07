from hypothesis.strategies import (
    SearchStrategy,
    composite,
    sampled_from,
    text,
    lists,
    integers,
)
from hypothesis import strategies as st
from typing import Callable
import string
import us
from .datatype import Vote, Election, Voter

TEST_ELECTION_ID = "fake_test_election"
CANDIDATE_POOL = ["Alice", "Bob", "Charlie", "David", "Eve"]


@st.composite
def voter_gen(draw) -> Voter:
    voter_id = draw(st.text(min_size=1, max_size=10, alphabet=string.ascii_letters))
    password = draw(st.text(min_size=1, max_size=10, alphabet=string.ascii_letters))
    age = draw(st.integers(min_value=18, max_value=120))
    gender = draw(st.sampled_from(["male", "female", "nonbinary", "other"]))
    region = draw(st.sampled_from([state.name for state in us.states.STATES]))
    race = draw(st.sampled_from(["Asian", "White", "Black", "Hispanic", "Other"]))
    education = draw(
        st.sampled_from(["unknown", "highschool", "bachelor", "master", "phd"])
    )
    return Voter(
        voter_id=voter_id,
        password=password,
        age=age,
        gender=gender,
        region=region,
        race=race,
        education=education,
        is_real=False,
        is_admin=False,
    )


@composite
def vote_gen(draw, election_id, candidate_pool) -> tuple[Voter, Vote]:
    voter = draw(voter_gen())
    return voter, Vote(
        election_id=election_id,
        candidate_name=draw(sampled_from(candidate_pool)),
        voter_id=voter.voter_id,
        is_real=False,
    )


def vote_list_gen(election_id, candidate_pool):
    return lists(
        vote_gen(election_id=election_id, candidate_pool=candidate_pool),
        min_size=50,
        max_size=100,
    )


def generate_votes(election_id, candidate_pool) -> list[tuple[Voter, Vote]]:
    return vote_list_gen(election_id, candidate_pool).example()  # type: ignore

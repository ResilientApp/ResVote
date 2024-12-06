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
    is_real = draw(st.just(False))
    is_admin = draw(st.just(False))

    return Voter(
        voter_id=voter_id,
        password=password,
        age=age,
        gender=gender,
        region=region,
        race=race,
        education=education,
        is_real=is_real,
        is_admin=is_admin,
    )


@composite
def vote_gen(draw) -> tuple[Voter, Vote]:
    voter = draw(voter_gen())
    return voter, Vote(
        election_id=TEST_ELECTION_ID,
        candidate_name=draw(sampled_from(CANDIDATE_POOL)),
        voter_id=voter.voter_id,
    )


vote_list_gen = lists(vote_gen(), min_size=50, max_size=100)

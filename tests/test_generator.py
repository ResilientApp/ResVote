import fire
from hypothesis import given
from hypothesis.strategies import lists

from src.datatype import Vote, Voter
from src.resdb import ResDBServer
from src.generator import generate_votes


def main() -> None:
    TEST_ELECTION_ID = "election_123"
    CANDIDATE_POOL = ["Alice", "Bob", "Charlie"]

    vs = generate_votes(TEST_ELECTION_ID, CANDIDATE_POOL)

    for voter, vote in vs:
        print(voter)
        print(vote)


if __name__ == "__main__":
    fire.Fire(main)

import fire
from hypothesis import given
from hypothesis.strategies import lists

from src.datatype import Vote, Voter
from src.resdb import ResDBServer
from src.generator import vote_list_gen


def generate_votes() -> list[tuple[Voter, Vote]]:
    return vote_list_gen.example()


def main(config_path: str = "config.yaml") -> None:
    vs = generate_votes()

    for voter, vote in vs:
        print(voter)
        print(vote)
        print("========")


if __name__ == "__main__":
    fire.Fire(main)

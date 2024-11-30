from resdb_orm import ResDBORM
import fire
import json
from hypothesis import given
from hypothesis.strategies import lists

from src.datatype import Vote
from src.vote_server import VoteServer
from src.generator import vote_list_gen


def generate_votes() -> list[Vote]:
    return vote_list_gen.example()


def main(config_path: str = "config.yaml", server_log_path: str | None = None) -> None:
    server = VoteServer(config_path, server_log_path)
    vs = generate_votes() 
    ids = server.create_all(vs)
    print(server.record_ids)
    all_ = server.read_all()
    for a in all_:
        print(a)
    

if __name__ == "__main__":
    fire.Fire(main)

from resdb_orm import ResDBORM
import fire
import json

from src.datatype import Vote
from src.vote_server import VoteServer


def main(config_path: str = "config.yaml", server_log_path: str | None = None) -> None:
    server = VoteServer(config_path, server_log_path)
    v1 = Vote(session_id="test_vote_1", candidate="1", voter_id="1122")
    v2 = Vote(session_id="test_vote_1", candidate="1", voter_id="1323")
    v3 = Vote(session_id="test_vote_1", candidate="2", voter_id="1122")
    
    _ = server.create_all([v1, v2, v3])
    
    all_ = server.read_all()
    for a in all_:
        print(a)
    

if __name__ == "__main__":
    fire.Fire(main)

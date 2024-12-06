from resdb_orm import ResDBORM
import fire
import json
from dataclasses import asdict
from hypothesis import given
from hypothesis.strategies import lists

from src.datatype import Vote
from src.vote_server import VoteServer
from src.generator import vote_list_gen
from src.json_utils import save_votes_to_json
from src.visualization import visualize_votes

def generate_votes() -> list[Vote]:
    return vote_list_gen.example()


def main(config_path: str = "config.yaml", server_log_path: str | None = None, output_json: str = "data/random_output.json") -> None:
    server = VoteServer(config_path, server_log_path)
    vs = generate_votes() 
    ids = server.create_all(vs)
    print(server.record_ids)
    all_ = server.read_all()
    
    # Export the vote data to a JSON file
    save_votes_to_json(all_, output_json)
    visualize_votes(all_, "vote_chart.png")
       
    for a in all_:
        print(a)
    

if __name__ == "__main__":
    fire.Fire(main)

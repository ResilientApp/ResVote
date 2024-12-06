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
from src.visualization import (
    plot_candidate_distribution,
    plot_attribute_distribution,
    plot_stacked_bar,
    plot_time_series
)

def generate_votes() -> list[Vote]:
    return vote_list_gen.example()


def main(config_path: str = "config.yaml", server_log_path: str | None = None, output_json: str = "data/random_output.json") -> None:
    server = VoteServer(config_path, server_log_path)
    vs = generate_votes() 
    ids = server.create_all(vs)
    print(server.record_ids)
    all_ = server.read_all()
        # for a in all_:
        # print(a)
    # Export the vote data to a JSON file
    save_votes_to_json(all_, output_json)
    # Different Visualization
    # Load the JSON data file
    with open(output_json, "r", encoding="utf-8") as f:
        votes = json.load(f)

    # votes is a list of vote records as described
    # Now we call the visualization functions with the loaded data

    # 1. Candidate Vote Distribution (Bar Chart)
    plot_candidate_distribution(votes, output_image="candidate_distribution.png")

    # 2. Attribute Distribution (Pie/Donut Chart)
    # Example: Distribution of gender
    plot_attribute_distribution(votes, attribute="gender", output_image="gender_distribution.png")

    # 3. Multi-dimension Analysis (Stacked Bar)
    # Example: gender + region combined
    plot_stacked_bar(votes, attribute1="gender", attribute2="region", output_image="stacked_bar.png")

    # 4. Time Series Analysis (Line Chart)
    plot_time_series(votes, output_image="time_series.png", freq='H')

    # After running main.py, you will find the generated charts in the current directory
 

    

if __name__ == "__main__":
    fire.Fire(main)

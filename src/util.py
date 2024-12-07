import os
import yaml
from returns.maybe import Maybe, Some, Nothing


def load_server_config(config_path: str) -> Maybe[tuple[str, int]]:
    if not os.path.exists(config_path):
        return Nothing

    with open(config_path, "r") as fp:
        config_data = yaml.safe_load(fp)

    host = config_data["vote_server"]["host"]
    port = config_data["vote_server"]["port"]
    return Some((host, port))


def to_vote_id(election_id: str, voter_id: str) -> str:
    return f"{election_id}++{voter_id}"

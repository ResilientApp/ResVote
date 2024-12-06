import json
from dataclasses import asdict
from typing import List
from .datatype import Vote


def save_votes_to_json(votes: List[Vote], filename: str) -> None:
    """Convert a list of Vote objects into JSON format and save to a file."""
    votes_dict_list = [asdict(v) for v in votes]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(votes_dict_list, f, ensure_ascii=False, indent=2)


def load_votes_from_json(filename: str) -> List[Vote]:
    """Load data from a JSON file and convert it into a list of Vote objects."""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Vote(**item) for item in data]

import json
from dataclasses import asdict
from typing import List, Optional
from .datatype import Vote
import os


def save_votes_to_json(votes: List[Vote], filename: str) -> None:
    """Convert a list of Vote objects into JSON format and save to a file."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    votes_dict_list = [asdict(v) for v in votes]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(votes_dict_list, f, ensure_ascii=False, indent=2)


def load_votes_from_json(filename: str) -> List[Vote]:
    """Load data from a JSON file and convert it into a list of Vote objects."""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Vote(**item) for item in data]


def save_voters_to_json(voters: List[Voter], filename: str) -> None:
    """Save a list of Voter objects to a JSON file, ensuring the directory exists."""
    # Ensure the directory for the file exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    voters_dict_list = [voter.__dict__ for voter in voters]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(voters_dict_list, f, ensure_ascii=False, indent=2)

def load_voters_from_json(filename: str) -> List[Voter]:
    """Load a list of Voter objects from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            voter_dict_list = json.load(f)
        return [Voter(**voter_dict) for voter_dict in voter_dict_list]
    except FileNotFoundError:
        return []

def get_voter(voter_id: str, voters: List[Voter]) -> Optional[Voter]:
    """Fetch a voter by voter_id."""
    for voter in voters:
        if voter.voter_id == voter_id:
            return voter
    return None
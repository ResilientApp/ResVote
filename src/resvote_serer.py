"""resVote Backend Server
"""

from .vote_server import VoteServer


class resVoteServer:
    def __init__(self) -> None:
        # self.vote_server = VoteServer(config_path, log_path)
        self.recorded_users: dict[str, str] = {}

    def register(self, username: str, password: str) -> bool:
        """Register a new user. If the user already exists, return False."""
        if username in self.recorded_users:
            return False

        self.recorded_users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        """Login a user.
        If the user does not exist or the password is incorrect,
        return False.
        """
        if username not in self.recorded_users:
            return False

        if self.recorded_users[username] != password:
            return False

        return True

    def get_elections(self) -> list[str]:
        """Get a list of election IDs."""
        # ToDo - query elections from the VoteServer
        election_ids = ["PRESIDENTIAL_2024_PRIMARIES", "PRESIDENTIAL_2024_GENERAL"]
        return election_ids

    def get_candidates(self, election_id: str) -> list[str]:
        """Get a list of candidate names for a given election."""
        # ToDo - query candidates from the VoteServer
        candidates: list[str] = []
        match election_id:
            case "PRESIDENTIAL_2024_PRIMARIES":
                candidates = ["Alice", "Bob", "Charlie"]
            case "PRESIDENTIAL_2024_GENERAL":
                candidates = ["David", "Eve"]
            case _:
                pass

        return candidates

    def vote(self, election_id: str, candidate_name: str, voter_id: str) -> bool:
        """Cast a vote for a candidate in an election."""
        # ToDo - create a Vote object and send it to the VoteServer
        return True

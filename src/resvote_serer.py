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

"""resVote Backend Server
"""

from .resdb import ResDBServer
from .datatype import Vote, Voter, Election


class resVoteServer:
    def __init__(self, config_path: str) -> None:
        self.resdb = ResDBServer(config_path)

        # NOTE: store everything in memory for now
        # should consider using a database in the future
        self.users: dict[str, Voter] = {}
        self.admins: dict[str, Voter] = {}
        self.elections: dict[str, Election] = {}
        self.votes: dict[str, Vote] = {}

    def register(self, username: str, password: str, is_admin: bool) -> bool:
        """Register a new user. If the user already exists, return False."""
        record_dict = self.admins if is_admin else self.users
        if username in record_dict:
            return False

        # add user to local cache
        new_user = Voter(voter_id=username, password=password)
        record_dict[username] = new_user
        # add user in ResDB
        # ! ignoring whether the record is created successfully for now
        _ = self.resdb.create(new_user)

        return True

    def login(self, username: str, password: str, is_admin: bool) -> bool:
        """Login a user.
        If the user does not exist or the password is incorrect,
        return False.
        """
        record_dict = self.admins if is_admin else self.users
        if username not in record_dict:
            return False

        # NOTE: should send request to ResDB to verify the password for security reasons
        # ! ignoring the verification for now
        if record_dict[username].password != password:
            return False

        return True

    def create_election(self, creator: str, election_id: str, candidates: str) -> bool:
        """Create a new election.
        candidates is string separated by comma.
        If the election already exists, return False.
        If the creator is not an admin, return False.
        """
        # check if creator is an admin
        if creator not in self.admins:
            return False

        if election_id in self.elections:
            return False

        candidates_list = candidates.split(",")
        new_election = Election(
            election_id=election_id,
            candidates=candidates_list,
            creator=creator,
        )

        # add election to local cache
        self.elections[election_id] = new_election
        # add election in ResDB
        # ! ignoring whether the record is created successfully for now
        _ = self.resdb.create(new_election)
        return True

    def get_elections(self) -> list[str]:
        """Get a list of election IDs."""
        return list(self.elections.keys())

    def get_candidates(self, election_id: str) -> list[str]:
        """Get a list of candidate names for a given election."""
        # ToDo - query candidates from the ResDBServer
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
        # ToDo - create a Vote object and send it to the ResDBServer
        return True

    def visualization(self, election_id: str):
        # ToDo - query visualization data from the ResDBServer
        pass

    def generation_votes(self, election_id: str):
        # ToDo - query generation votes from the ResDBServer
        pass

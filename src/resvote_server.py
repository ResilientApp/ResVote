"""resVote Backend Server
"""

from .resdb import ResDBServer
from .datatype import Vote, Voter, Election
from .generator import generate_votes
from tqdm import tqdm


class resVoteServer:
    def __init__(self, config_path: str) -> None:
        self.resdb = ResDBServer(config_path)

        # NOTE: store everything in memory for now
        # should consider using a database in the future
        self.users: dict[str, Voter] = {}
        self.elections: dict[str, Election] = {}
        self.votes: dict[str, Vote] = {}

        self._load__from_resdb()

    def _load__from_resdb(self):
        print("loading history data from ResDB")
        all_data = self.resdb.db_read_all()

        for d in tqdm(all_data):
            if d["type"] == "Voter":
                self.users[d["id"]] = Voter(**d["data"])
            elif d["type"] == "Election":
                self.elections[d["id"]] = Election(**d["data"])
            elif d["type"] == "Vote":
                self.votes[d["id"]] = Vote(**d["data"])

    def register(self, username: str, password: str, is_admin: bool) -> bool:
        """Register a new user. If the user already exists, return False."""
        if username in self.users:
            return False

        # add user to local cache
        new_user = Voter(voter_id=username, password=password, is_admin=is_admin)
        self.users[new_user.transaction_id] = new_user
        # add user in ResDB
        # ! ignoring whether the record is created successfully for now
        _ = self.resdb.create(new_user)

        return True

    def login(self, username: str, password: str) -> bool:
        """Login a user.
        If the user does not exist or the password is incorrect,
        return False.
        """
        if username not in self.users:
            return False

        # NOTE: should send request to ResDB to verify the password for security reasons
        # ! ignoring the verification for now
        if self.users[username].password != password:
            return False

        return True

    def create_election(self, creator: str, election_id: str, candidates: str) -> bool:
        """Create a new election.
        candidates is string separated by comma.
        If the election already exists, return False.
        If the creator is not an admin, return False.
        """
        # check if creator is an admin
        if creator not in self.users and not self.users[creator].is_admin:
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
        self.elections[new_election.transaction_id] = new_election
        # add election in ResDB
        # ! ignoring whether the record is created successfully for now
        _ = self.resdb.create(new_election)
        return True

    def get_elections(self) -> list[str]:
        """Get a list of election IDs."""
        return list(self.elections.keys())

    def get_candidates(self, election_id: str) -> list[str]:
        """Get a list of candidate names for a given election."""
        if election_id not in self.elections:
            return []

        candidates = self.elections[election_id].candidates
        return candidates

    def create_vote(self, voter_id: str, election_id: str, candidate_name: str) -> bool:
        """Cast a vote for a candidate in an election.
        if the election, candidate, or voter does not exist, return False.
        If the voter has already voted in this election, return False.
        """
        if election_id not in self.elections:
            print(f"election_id {election_id} not in self.elections")
            return False

        if candidate_name not in self.elections[election_id].candidates:
            print(f"candidate_name {candidate_name} not in self.elections")
            return False

        # NOTE: admin can also vote
        if voter_id not in self.users and not self.users[voter_id].is_admin:
            print(f"voter_id {voter_id} not in the users")
            return False

        new_vote = Vote(
            election_id=election_id,
            candidate_name=candidate_name,
            voter_id=voter_id,
        )

        if new_vote.transaction_id in self.votes:
            return False

        # add vote to local cache
        self.votes[new_vote.transaction_id] = new_vote
        # add vote in ResDB
        # ! ignoring whether the record is created successfully for now
        _ = self.resdb.create(new_vote)
        return True

    def get_votes(self, election_id: str) -> list[Vote]:
        """Get a list of votes for a given election."""
        return [vote for vote in self.votes.values() if vote.election_id == election_id]

    def visualization(self, election_id: str):
        # ToDo - query visualization data from the ResDBServer
        pass

    def generate_random_votes(self, election_id: str) -> bool:
        """generate fake votes for visualization and testing"""

        if election_id not in self.elections:
            return False

        vs = generate_votes(election_id, self.elections[election_id].candidates)

        for voter, vote in vs:
            if voter.voter_id not in self.users:
                self.users[voter.voter_id] = voter
                _ = self.resdb.create(voter)

                self.votes[vote.transaction_id] = vote
                _ = self.resdb.create(vote)

        return True

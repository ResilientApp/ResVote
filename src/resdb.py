"""
A wrapper class for ResDBORM to manage Vote data records,
with some helper functions and better error handling.
"""

from resdb_orm import ResDBORM
from dataclasses import asdict
import logging
from returns.maybe import Maybe, Some, Nothing
from typing import Any
import requests
import json
from collections import Counter

from .datatype import Vote, Voter, Election


class ResDBServer:
    def __init__(self, config_path: str, log_path: str | None = None) -> None:
        self.db = ResDBORM(config_path)
        self.record_ids: set[str] = set()

    def __del__(self) -> None:
        self.delete_all()

    def create(self, vote: Vote | Voter | Election) -> Maybe[str]:
        """create a single vote record in the DB,
        modified based on the original create method from resdb-orm

        Args:
            vote (Vote): the vote record to be created

        Returns:
            Maybe[str]: the record id if successful, Nothing otherwise
        """
        payload = {"id": vote.transaction_id, "data": asdict(vote)}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(
                f"{self.db.db_root_url}/v1/transactions/commit",
                data=json.dumps(payload),
                headers=headers,
            )
        except Exception as e:
            logging.warning(f"ResDBServer.create: request error {e}")
            return Nothing

        # Check if response is successful and handle empty response content
        if response.status_code != 201:
            return Nothing
        if not response.content:
            return Nothing
        decoded_content = response.content.decode("utf-8")
        id_value = decoded_content.split(": ")[1].strip()

        return Some(id_value)

    def create_all(self, votes: list[Vote] | list[Voter]) -> list[Maybe[str]]:
        """create multiple vote records in the DB

        Args:
            votes (list[Vote]): a list of vote records to be created

        Returns:
            list[str]: a list of record ids
        """
        return list(map(self.create, votes))

    def read(self, transaction_id: str) -> Maybe[dict[str, Any]]:
        """read a single vote record from the DB

        Args:
            transaction_id (str): the record id to be read

        Returns:
            Maybe[Vote]: the vote record if successful, Nothing otherwise
        """
        try:
            response = self.db.read(transaction_id)
        except Exception as e:
            logging.warning(f"ResDBServer.read: request error {e}")
            return Nothing

        if not isinstance(response, dict):
            if isinstance(response, str):
                logging.warning(f"ResDBServer.read: {response}")
            else:
                logging.warning("ResDBServer.read: unknown error from ResDB.")
            return Nothing

        try:
            assert transaction_id == response["id"]
            vote_data = response["data"]
        except KeyError as e:
            logging.warning(f"ResDBServer.read: KeyError {e}")
            return Nothing

        return Some(vote_data)

    def db_read_all(self) -> Any:
        """read all data records from the DB, no matter if it is created by this server or not

        Returns:
            list[Vote]: a list of Vote objects
        """
        try:
            response = self.db.read_all()
        except Exception as e:
            logging.warning(e)
            return None

        return response

    def delete_all(self):
        """delete all data records managed by this server"""

        for rid in self.record_ids:
            response = self.db.delete(rid)
            if (
                isinstance(response, dict)
                and "status" in response
                and response["status"] != "delete successful"
            ):
                logging.warning(response["status"])

    def db_delete_all(self):
        """delete all data records in the DB"""
        try:
            response = self.db.read_all()
        except Exception as e:
            logging.warning(e)
            return

        for record in response:
            self.db.delete(record["id"])

    # def get(self, election_id: str, voter_id: str) -> Maybe[Vote]:
    #     """Retrieve a vote by election_id and voter_id.

    #     Args:
    #         election_id (str): The election ID.
    #         voter_id (str): The voter ID.

    #     Returns:
    #         Maybe[Vote]: The corresponding Vote object if found, Nothing otherwise.
    #     """
    #     for record_id in self.record_ids:
    #         vote = self.read(record_id).unwrap_or(None)
    #         if vote and vote.election_id == election_id and vote.voter_id == voter_id:
    #             return Some(vote)
    #     return Nothing

    # def total_votes(self, election_id: str) -> int:
    #     """Get the total number of votes in an election.

    #     Args:
    #         election_id (str): The election ID.

    #     Returns:
    #         int: Total number of votes in the election.
    #     """
    #     return sum(
    #         1
    #         for record_id in self.record_ids
    #         if self.read(record_id).unwrap_or(None)
    #         and self.read(record_id).unwrap().election_id == election_id
    #     )

    # def votes_per_candidate(self, election_id: str) -> dict[str, int]:
    #     """Get the number of votes each candidate received in an election.

    #     Args:
    #         election_id (str): The election ID.

    #     Returns:
    #         dict[str, int]: A dictionary with candidates as keys and their vote counts as values.
    #     """
    #     candidate_votes = Counter()
    #     for record_id in self.record_ids:
    #         vote = self.read(record_id).unwrap_or(None)
    #         if vote and vote.election_id == election_id:
    #             candidate_votes[vote.candidate] += 1
    #     return dict(candidate_votes)

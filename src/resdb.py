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
    def __init__(self, config_path: str) -> None:
        self.db = ResDBORM(config_path)

    def create(self, data: Vote | Voter | Election) -> Maybe[str]:
        """create a single vote record in the DB,
        modified based on the original create method from resdb-orm

        Args:
            vote (Vote): the vote record to be created

        Returns:
            Maybe[str]: the record id if successful, Nothing otherwise
        """
        payload = {
            "id": data.transaction_id,
            "data": asdict(data),
            "type": type(data).__name__,
        }
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


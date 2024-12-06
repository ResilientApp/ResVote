from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import fire
from src.util import load_server_config
import logging


recorded_users: dict[str, str] = {}


def register(username, password):
    """register a new user. If the user already exists, return False."""
    if username in recorded_users:
        logging.info(f"User {username} already exists.")
        return False

    logging.info(f"Registering user {username}.")
    recorded_users[username] = password
    return True


def login(username, password) -> bool:
    """login a user. If the user does not exist or the password is incorrect, return False."""
    if username not in recorded_users:
        logging.info(f"User {username} does not exist.")
        return False

    if recorded_users[username] != password:
        logging.info(f"Password for user {username} is incorrect.")
        return False

    logging.info(f"User {username} logged in.")
    return True


def serve(config_path: str = "config.yaml"):
    logging.basicConfig(level=logging.WARNING)

    host, port = load_server_config(config_path).unwrap()

    logging.info(f"Starting server on {host}:{port}")
    with SimpleXMLRPCServer(
        (host, port), requestHandler=SimpleXMLRPCRequestHandler
    ) as server:
        server.register_introspection_functions()

        server.register_function(register, "register")
        server.register_function(login, "login")

        server.serve_forever()


if __name__ == "__main__":
    fire.Fire(serve)

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import fire
from src.util import load_server_config
import logging


def add(x, y):
    return x + y


def mul(x, y):
    return x * y


def serve(config_path: str = "config.yaml"):
    logging.basicConfig(level=logging.INFO)

    host, port = load_server_config(config_path).unwrap()

    logging.info(f"Starting server on {host}:{port}")
    with SimpleXMLRPCServer(
        (host, port), requestHandler=SimpleXMLRPCRequestHandler
    ) as server:
        server.register_introspection_functions()

        server.register_function(add, "add")
        server.register_function(mul, "mul")

        server.serve_forever()


if __name__ == "__main__":
    fire.Fire(serve)

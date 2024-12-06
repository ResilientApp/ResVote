from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import fire
import logging
import sys
from src.util import load_server_config
from src.resvote_server import resResDBServer


def serve(config_path: str = "config.yaml"):
    logging.basicConfig(level=logging.WARNING)

    host, port = load_server_config(config_path).unwrap()

    logging.info(f"Starting server on {host}:{port}")
    with SimpleXMLRPCServer(
        (host, port), requestHandler=SimpleXMLRPCRequestHandler
    ) as server:
        server.register_introspection_functions()
        server.register_instance(resResDBServer())

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


if __name__ == "__main__":
    fire.Fire(serve)

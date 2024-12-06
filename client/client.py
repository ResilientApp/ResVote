import xmlrpc.client
import fire
from src.util import load_server_config


def main(config_path: str = "config.yaml"):
    host, port = load_server_config(config_path).unwrap()
    s = xmlrpc.client.ServerProxy("http://localhost:8000")
    print(s.add(2, 3))  # Returns 5
    print(s.mul(5, 2))  # Returns 5*2 = 10

    # Print list of available methods
    print(s.system.listMethods())


if __name__ == "__main__":
    fire.Fire(main)

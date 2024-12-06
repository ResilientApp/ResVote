import xmlrpc.client
import fire
from src.util import load_server_config


def main(config_path: str = "config.yaml"):
    host, port = load_server_config(config_path).unwrap()

    url = f"http://{host}:{port}"
    s = xmlrpc.client.ServerProxy(url)

    print(s.get_elections())


if __name__ == "__main__":
    fire.Fire(main)

# type: ignore
import xmlrpc.client
import fire
from src.util import load_server_config


def main(config_path: str = "config.yaml"):
    host, port = load_server_config(config_path).unwrap()

    url = f"http://{host}:{port}"
    s = xmlrpc.client.ServerProxy(url)

    username = "yfhe"
    password = "aaaa"

    s.register(username, password)
    s.login(username, password)

    election_ids: list[str] = s.get_elections()
    print(election_ids)

    for election_id in election_ids:
        print(election_id)
        candidates = s.get_candidates(election_id)
        print(candidates)


if __name__ == "__main__":
    fire.Fire(main)

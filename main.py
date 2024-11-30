from resdb_orm import ResDBORM
import fire

def main(config_path: str = "config.yaml"):
    db = ResDBORM(config_path)
    
    data = {"name": "abc", "age": 123}
    create_response = db.create(data)
    print("Create Response:", create_response)
    
    all_ = db.read_all()
    print(all_)

if __name__ == "__main__":
    fire.Fire(main)

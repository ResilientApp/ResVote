# resVoteGenerator

Random vote generator based on property-based testing

## Python

We recommand using `conda` to manage python environment.

```sh
conda create -n "resdb" python=3.10.0 ipython
conda activate resdb
pip install -r requirements.txt
```

## Get ResilientDB Dependencies

### ResilientDB

The following commands will clone and build ResilientDB,
and then starts 4 replicas and 1 client. Each replica instantiates a key-value store.

```sh
git clone https://github.com/apache/incubator-resilientdb.git resilientdb
cd resilientdb
./INSTALL.sh
./service/tools/kv/server_tools/start_kv_service.sh
```

### Graph QL

```sh
git clone https://github.com/apache/incubator-resilientdb-graphql.git resilientdb-graphql
cd resilientdb-graphql
sh ./INSTALL.sh
pip install -r requirements.txt
sh service/tools/start_kv_service_sdk.sh
```

#### Running Crow service (HTTP endpoints)

```sh
bazel build service/http_server/crow_service_main
bazel-bin/service/http_server/crow_service_main service/tools/config/interface/client.config service/http_server/server_config.config
```

#### Test if SDK and service are working

```sh
python test_driver.py 
```

## Running this project

```sh
source ./env.sh
python main.py
```

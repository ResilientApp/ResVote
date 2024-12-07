# resVote

Random vote generator based on property-based testing

## Python

We recommend using `conda` to manage python environment.

```sh
conda create -n "resdb" python=3.10.0 ipython
conda activate resdb
pip install -r requirements.txt
```

## Get ResilientDB Dependencies

To save some time, we also provide a docker image that has all the dependencies installed.

```sh
docker pull yfhecs/rsdb
docker run -d -p 18000:18000 --name resdb yfhecs/rsdb
```
If you choose to use docker, you can skip the following steps.
Please wait a few minutes for the docker container to start.
You can check if it is ready by the follow command:

```sh
❯ curl -X POST -d '{"id":"key1","value":"value1"}' localhost:18000/v1/transactions/commit
id: key1

❯ curl 127.0.0.1:18000/v1/transactions/key1
{"id":"key1","value":"value1"}
```

You can also find the related dockerfile in the `./docker` directory.


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

## resVote Server

```sh
source ./env.sh
python app/serve.py
```

## resVote TUI Client

```sh
source ./env.sh
python app/tui.py
```
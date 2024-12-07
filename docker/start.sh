#!/bin/bash
# start resilient db
cd resilientdb && ./service/tools/kv/server_tools/start_kv_service.sh
cd ..

# start graph ql
cd resilientdb-graphql
nohup bazel-bin/service/http_server/crow_service_main service/tools/config/interface/service.config service/http_server/server_config.config
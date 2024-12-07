FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    vim \
    libssl-dev \
    git \
    sudo \
    apt-transport-https \
    gnupg \
    python3-pip

# install bazel
RUN curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg
RUN mv bazel-archive-keyring.gpg /usr/share/keyrings
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
RUN apt-get update && apt-get install -y bazel

# ------------------------------------------------------

    # compile and setup ResilientDB
WORKDIR /app
RUN git clone https://github.com/apache/incubator-resilientdb resilientdb
WORKDIR /app/resilientdb
RUN sh INSTALL.sh
RUN bazel build service/tools/kv/api_tools/kv_service_tools

# ------------------------------------------------------

    # compile and setup ResilientDB-GraphQL
WORKDIR /app
RUN git clone https://github.com/apache/incubator-resilientdb-graphql.git resilientdb-graphql
WORKDIR /app/resilientdb-graphql

# Build Crow HTTP server
RUN bazel build service/http_server:crow_service_main

# Setup Python environment
RUN pip3 install -r requirements.txt

# ------------------------------------------------------

WORKDIR /app
COPY start.sh /app/start.sh
# start the services
CMD ["/app/start.sh"]

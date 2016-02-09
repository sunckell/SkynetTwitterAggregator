#!/bin/bash

DOCKER_ENV_ARGS=""
for ENV_ARG in `curl http://169.254.169.254/latest/user-data`
do
 DOCKER_ENV_ARGS="${DOCKER_ENV_ARGS} -e ${ENV_ARG}"
done

docker daemon --log-driver=awslogs ---log-opt awslogs-region=us-east-1

docker run --label foo=bar ${DOCKER_ENV_ARGS} -d -P sunckell/skynettwitteraggregator python3 /src/skynet-twitter-aggregator.py
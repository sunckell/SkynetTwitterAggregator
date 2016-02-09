#!/bin/bash

for i in `curl http://169.254.169.254/latest/user-data`
do
 export $i
done

python3 /src/skynet-twitter-aggregator.py

docker daemon --log-driver=awslogs ---log-opt awslogs-region=us-east-1

docker run --label foo=bar -e fizz=buzz -d -P sunckell/skynettwitteraggregator python3 /src/skynet-twitter-aggregator.py
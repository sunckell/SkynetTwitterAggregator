#!/bin/bash

for i in `curl http://169.254.169.254/latest/user-data`
do
 export $i
done

python3 /src/skynet-twitter-aggregator.py
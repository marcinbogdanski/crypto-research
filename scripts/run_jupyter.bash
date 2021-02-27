#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "You must specify path to data folder!"
    exit 1
fi

DATAPATH=$(realpath $1)

docker run -it --rm \
  -p 9997:9997 \
  -v $PWD:/app \
  -v $DATAPATH:/mnt/data:ro \
  -w / \
  --entrypoint=jupyter \
  --env-file=dotenv-scan-3060ti.env \
  crypto-research lab \
    --ip=0.0.0.0 --port=9997 --allow-root

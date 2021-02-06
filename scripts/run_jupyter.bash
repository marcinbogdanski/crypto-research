#!/bin/bash

docker run -it --rm \
  -p 9997:9997 \
  -v /home/marcin/crypto-research:/app \
  --entrypoint=jupyter \
  ml-deployment lab \
    --ip=0.0.0.0 --port=9997 --allow-root

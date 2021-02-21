#!/bin/bash

docker run -it --rm \
  -p 9997:9997 \
  -v /home/marcin/crypto-research:/app \
  --entrypoint=jupyter \
  --env-file=dotenv-scan-3060ti.env \
  crypto-research lab \
    --ip=0.0.0.0 --port=9997 --allow-root

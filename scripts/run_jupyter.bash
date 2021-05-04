#!/bin/bash

# if [ "$#" -ne 1 ]; then
#     echo "You must specify path to data folder!"
#     exit 1
# fi

# DATAPATH=$(realpath $1)

docker run -it --rm \
  -p 9997:9997 \
  -v $PWD:/app \
  --network=host \
  --entrypoint=jupyter \
  --env-file=dotenv.env \
  crypto-research lab \
    --ip=0.0.0.0 --port=9997


# Other options:
# -u "$(id -u):$(id -g)" \
# -w / \
# --network=host \         - able to talk to other services on localhost
# --network=my-network \
# -v $DATAPATH:/mnt/data:ro \        - attach data folder
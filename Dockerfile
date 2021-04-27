FROM ubuntu:focal-20210416

# VPN Dependencies
# psmisc - killall
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nano psmisc unzip wget openvpn

# Network Utils nad UFW
# curl - curl
# dnsutils - dig, nslookup
# iputils-ping - ping
# net-tools - route
# traceroute - traceroute
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl dnsutils iputils-ping net-tools traceroute ufw

# Python 3
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip

# Get VPN config files
WORKDIR /root
RUN wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip
RUN unzip ovpn.zip

# Third Party
RUN pip3 install beautifulsoup4==4.9.3
RUN pip3 install boto3==1.17.13
RUN pip3 install lxml==4.6.2
RUN pip3 install pymongo==3.11.3
RUN pip3 install smart-open==4.2.0
RUN pip3 install tqdm==4.58.0

# Development
RUN pip3 install pylint
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git

ENV PYTHONPATH="/app"

WORKDIR /app
COPY . /app

ENTRYPOINT [ "/app/scripts/startup.bash" ]

# Build like this:
# docker build -t gpu-scrapper .

# Run like this:
# docker run -it --rm --cap-add NET_ADMIN --env-file dotenv.env gpu-scrapper

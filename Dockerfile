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

# Install Python 3
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip

# Get VPN config files
WORKDIR /root
RUN wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip
RUN unzip ovpn.zip

# Switch to Python 3
# source: https://unix.stackexchange.com/questions/410579/change-the-python3-default-version-in-ubuntu/410851
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN ln -s /usr/bin/pip3 /usr/bin/pip

# Third Party
RUN pip install beautifulsoup4==4.9.3
RUN pip install boto3==1.17.13
RUN pip install lxml==4.6.2
RUN pip install pymongo==3.11.3
RUN pip install smart-open==4.2.0
RUN pip install tqdm==4.58.0

# Development
RUN pip install pylint
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

FROM ubuntu:focal-20210416

# Utils and VPN Dependencies
RUN apt-get update && apt-get install -y \
  curl \
  jq \
  nano \
  unzip \
  wget \
  openvpn

# Network Utils
# dnsutils - dig, nslookup
# iputils-ping - ping
# net-tools - route
# psmisc - killall
# traceroute - traceroute
RUN apt-get update && apt-get install -y \
  dnsutils \
  iputils-ping \
  net-tools \
  psmisc \
  traceroute \
  ufw

WORKDIR /root
RUN wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip
RUN unzip ovpn.zip
 
WORKDIR /root
COPY . /root

ENTRYPOINT [ "/root/scripts/startup.bash" ]

# Build like this:
# docker build -t gpu-scrapper .

# Run like this:
# docker run -it --rm --cap-add NET_ADMIN --env-file dotenv.env gpu-scrapper

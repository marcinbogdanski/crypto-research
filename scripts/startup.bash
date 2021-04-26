#!/bin/bash

source scripts/add_dns_route.bash
source scripts/ufw_up.bash
source scripts/vpn_up.bash

sleep 5

while true; do
  date
  curl -s ipinfo.io
  echo
  echo
  sleep 1
done

# /root/ovpn_tcp/us8719.nordvpn.com.tcp.ovpn  192.145.119.142
# /root/ovpn_tcp/de999.nordvpn.com.tcp.ovpn    37.120.197.56

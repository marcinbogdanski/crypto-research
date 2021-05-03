#!/bin/bash

if [ $VPN_ENABLE == "true" ]; then
  echo "Adding DNS route, enabling UFW nad VPN"
  source scripts/add_dns_route.bash
  source scripts/ufw_up.bash
  source scripts/vpn_up.bash
elif [ $VPN_ENABLE == "false" ]; then
  echo "Leavnig DNS untouched, omitting UFW and VPN"
else
  echo "Variable VPN_ENABLE must be set to either 'true' or 'false'. Exiting"
  exit 1
fi

while true; do
  date
  curl -s ipinfo.io
  echo
  echo
  sleep 1
done

# /root/ovpn_tcp/us8719.nordvpn.com.tcp.ovpn  192.145.119.142
# /root/ovpn_tcp/de999.nordvpn.com.tcp.ovpn    37.120.197.56

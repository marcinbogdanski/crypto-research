#!/bin/bash

if [ $VPN_ENABLE == "true" ]; then
  echo "Startup: Adding DNS route, enabling UFW nad VPN"
  source scripts/add_dns_route.bash
  source scripts/ufw_up.bash
  source scripts/vpn_up.bash
elif [ $VPN_ENABLE == "false" ]; then
  echo "Startup: Leavnig DNS untouched, omitting UFW and VPN"
else
  echo "Startup: Variable VPN_ENABLE must be set to either 'true' or 'false'. Exiting"
  exit 1
fi

# Run actual program
echo "Startup: Executing 'python -m gpuscrapper.main'"
python -m gpuscrapper.main
RETURN_CODE=$?
echo "Startup: Main program exited"

if [ $VPN_ENABLE == "true" ]; then
  source scripts/vpn_down.bash
fi

exit $RETURN_CODE

# while true; do
#   date
#   curl -s ipinfo.io
#   echo
#   echo
#   sleep 1
# done

# /root/ovpn_tcp/us8719.nordvpn.com.tcp.ovpn  192.145.119.142
# /root/ovpn_tcp/de999.nordvpn.com.tcp.ovpn    37.120.197.56

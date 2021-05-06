#!/bin/bash

echo "VPN: Killing openvpn"
killall openvpn

echo "VPN: Waiting 5 seconds"
sleep 5

echo "VPN: Checking /tmp/openvpn.log"
echo "----------"
cat /tmp/openvpn.log
echo "----------"

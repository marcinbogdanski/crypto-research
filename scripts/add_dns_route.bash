#!/bin/bash

echo "----------"
echo "Entering script add_dns_route.bash"

echo "Executing: ip route show default"
ip route show default
DEFAULT_GATEWAY_PRE_VPN=$(ip route show default | awk '{print $3}')
echo "Extracted gateway: $DEFAULT_GATEWAY_PRE_VPN"

echo "Executing: cat /etc/resolv.conf"
cat /etc/resolv.conf
DNS_IP_ADDRESS_PRE_VPN=$(cat /etc/resolv.conf | grep -m1 nameserver | awk '{print $2}')
echo "Extracted DNS IP: $DNS_IP_ADDRESS_PRE_VPN"

echo "Establishing network range and mask"
DNS_FIRST_BYTE=$(echo $DNS_IP_ADDRESS_PRE_VPN | cut -d. -f1)
DNS_SECOND_BYTE=$(echo $DNS_IP_ADDRESS_PRE_VPN | cut -d. -f2)
echo "Extracted first two bytes: $DNS_FIRST_BYTE $DNS_SECOND_BYTE"
if [ $DNS_FIRST_BYTE == "192" ] && [ $DNS_SECOND_BYTE == "168" ]; then
    NETWORK_NEW="192.168.0.0"
    NETMASK_NEW="255.255.0.0"
elif [ $DNS_FIRST_BYTE == "169" ] && [ $DNS_SECOND_BYTE == "254" ]; then
    NETWORK_NEW="169.254.0.0"
    NETMASK_NEW="255.255.0.0"
elif [ $DNS_FIRST_BYTE == "10" ]; then
    NETWORK_NEW="10.0.0.0"
    NETMASK_NEW="255.0.0.0"
fi
echo "DNS seems to be on network $NETWORK_NEW with netmask $NETMASK_NEW"

echo "Executing: route add -net $NETWORK_NEW netmask $NETMASK_NEW gw $DEFAULT_GATEWAY_PRE_VPN"
route add -net $NETWORK_NEW netmask $NETMASK_NEW gw $DEFAULT_GATEWAY_PRE_VPN

echo "Exiting script add_dns_route.bash"
echo "----------"
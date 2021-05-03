#!/bin/bash

echo "Executing: ip route show default"
ip route show default
DEFAULT_INTERFACE=$(ip route show default | awk '{print $5}')
echo "Extracted default interface: $DEFAULT_INTERFACE"

echo "Executing: cat /etc/resolv.conf"
echo "----------"
cat /etc/resolv.conf
echo "----------"
DNS_IP_ADDRESS_PRE_VPN=$(cat /etc/resolv.conf | grep -m1 nameserver | awk '{print $2}')
echo "Extracted DNS IP: $DNS_IP_ADDRESS_PRE_VPN"

echo "Establishing network range and mask"
DNS_FIRST_BYTE=$(echo $DNS_IP_ADDRESS_PRE_VPN | cut -d. -f1)
DNS_SECOND_BYTE=$(echo $DNS_IP_ADDRESS_PRE_VPN | cut -d. -f2)
echo "Extracted first two bytes: $DNS_FIRST_BYTE $DNS_SECOND_BYTE"
if [ $DNS_FIRST_BYTE == "192" ] && [ $DNS_SECOND_BYTE == "168" ]; then
    NETWORK_NEW="192.168.0.0/16"
elif [ $DNS_FIRST_BYTE == "169" ] && [ $DNS_SECOND_BYTE == "254" ]; then
    NETWORK_NEW="169.254.0.0/16"
elif [ $DNS_FIRST_BYTE == "10" ]; then
    NETWORK_NEW="10.0.0.0/8"
else
    echo "Unknown network for this DNS: $$DNS_IP_ADDRESS_PRE_VPN, exiting"
    exit 1
fi

VPN_INTERFACE="tun0"

echo "Extracting VPN remote IP from $VPN_CONF"
VPN_REMOTE_IP=$(cat $VPN_CONF | grep "remote " | awk '{print $2}')
echo "Extracted VPN remote IP: $VPN_REMOTE_IP"

echo "Applying UFW rules to allow only VPN traffic"
ufw --force reset || exit
ufw default deny incoming || exit
ufw default deny outgoing || exit
echo "Executing: ufw allow out on $DEFAULT_INTERFACE from any to $VPN_REMOTE_IP"
ufw allow out on $DEFAULT_INTERFACE from any to $VPN_REMOTE_IP || exit
echo "Executing: ufw allow out on $DEFAULT_INTERFACE from any to $NETWORK_NEW"
ufw allow out on $DEFAULT_INTERFACE from any to $NETWORK_NEW || exit
ufw allow out on $VPN_INTERFACE from any to any || exit

echo "Enabling UFW"
ufw enable || exit

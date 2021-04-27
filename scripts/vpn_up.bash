#!/bin/bash

mkdir -p /dev/net
mknod /dev/net/tun c 10 200
chmod 600 /dev/net/tun

echo $VPN_USER >> /tmp/up
echo $VPN_PASS >> /tmp/up

# DNS
# On Ubuntu, DNS is defined in /etc/resolv.conf

# NOTE: This doesn't seem to affect /etc/resolv.conf
# NOTE: Inside container openvpn-systemd-resolved doesn't work due to dbus
# echo "" >> $VPN_CONF
# echo "script-security 2" >> $VPN_CONF
# echo "up /etc/openvpn/update-resolv-conf" >> $VPN_CONF
# echo "down /etc/openvpn/update-resolv-conf" >> $VPN_CONF

openvpn --config $VPN_CONF --auth-user-pass /tmp/up --log /tmp/openvpn.log --daemon

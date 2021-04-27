#!/bin/bash

echo "Applying UFW rule to allow all traffic"
ufw --force reset
ufw default deny incoming
ufw default allow outgoing

echo "Enabling UFW"
ufw enable

#!/bin/sh
cp ./services/80-can.network /lib/systemd/network/

systemctl stop systemd-networkd.service
systemctl start systemd-networkd.service
systemctl enable systemd-networkd.service
# cp ./servics/cs-canbus.service /lib/systemd/system

# sudo systemctl daemon-reload
# sudo systemctl enable cs-canbus.service
# sudo systemctl start cs-canbus.service
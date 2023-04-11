#!/bin/sh
sudo ip link set can0 up type can bitrate 1000000

echo "SocketCAN setup completed!"
# cityscope-canopen-controller
``` bash
sudo ifconfig can0 txqueuelen 10000
sudo ip link set can0 up type can bitrate 1000000
```

``` bash
sudo modprobe vcan
# Create a vcan network interface with a specific name(vcan0)
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up
```
[conn](https://github.com/CANopenNode/CANopenDemo/tree/master/tutorial)
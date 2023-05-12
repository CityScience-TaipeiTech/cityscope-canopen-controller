# cityscope-canopen-controller
``` bash
sudo ifconfig can0 txqueuelen 10000
sudo ip link set can0 up type can bitrate 1000000
```
<!-- [conn](https://github.com/CANopenNode/CANopenDemo/tree/master/tutorial) -->

### Record CAN bus data on `can0`
``` bash
candump -L can0 > cityscope_normal.log
```
### Play recorded CAN bus data on `vcan0`
1. Initial a virtual CAN interface.
    ``` bash
    sudo modprobe vcan
    # Create a vcan network interface with a specific name(vcan0)
    sudo ip link add dev vcan0 type vcan
    sudo ip link set vcan0 up
    ```
2. Play the recorded log.
    ``` bash
    canplayer vcan0=can0 -I ./test_data/cityscope_normal.log
    ```
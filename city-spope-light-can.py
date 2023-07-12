#!/usr/bin/python3
# sudo ifconfig can0 txqueuelen 10000
# sudo ip link set can0 up type can bitrate 1000000
import tomli
import time
import canopen


def main():
    network = canopen.Network()
    network.connect(channel="can0", bustype='socketcan')
    node = network.add_node(
        81, '/home/cityscpe/cityscope-canopen-controller/DS301_profile_mcu.eds')
    node.rpdo.read()
    node.nmt.state = 'PRE-OPERATIONAL'
    # print(node.rpdo.len())
    node.rpdo[1][0x6001].phys = 0
    node.rpdo[1].start(0.1)
    node.nmt.state = 'OPERATIONAL'
    return


if __name__ == "__main__":
    main()
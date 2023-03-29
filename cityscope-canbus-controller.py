#!/usr/bin/python3
import time
import canopen

def main():
    network = canopen.Network()
    network.connect(channel='can0', bustype='socketcan')
    node = network.add_node(21, '/home/justin/github/cityscope/cityscope-firmware/cityscope_proximity_controller/DS301_profile_mcu.eds')
    for node_id in network:
        print(network[node_id])
    # network.scanner.search()
    # time.sleep(0.05)
    # for node_id in network.scanner.nodes:
    #     print("Found node %d!" % node_id)
    node.tpdo.read()
    node.rpdo.read()
    def print_speed(message):
        print('%s received' % message.name)
        for var in message:
            print('%s = %d' % (var.name, var.raw, ))

    node.tpdo[1].add_callback(print_speed)
    time.sleep(5)
    network.disconnect()
    return

if __name__ == "__main__":
    main()
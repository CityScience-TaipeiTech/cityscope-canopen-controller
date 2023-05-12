#!/usr/bin/python3
import tomli
import time
import canopen
from cs_gesture_detector import CsGestureDetector

class CsCanOpen:
    def __init__(self, can_interface, config_file):
        self.node_list = []
        self.config = self.load_config(config_file)
        self.gesture = CsGestureDetector(self.config["gesrure"], self.config["proximity"])
        self.can_network = self.canopen_init(can_interface)
        self.load_nodes(self.config["proximity"])

    def load_config(self, config_file):
        with open(config_file, "rb") as f:
            toml_dict = tomli.load(f)
            return toml_dict

    def canopen_init(self, can_interface="can0"):
        network = canopen.Network()
        network.connect(channel=can_interface, bustype='socketcan')
        return network
    
    def load_nodes(self, config):
        node_set = {}
        for node in config["nodes"]:
            print("Wait for node {0:} ready...".format(node["node_id"]))
            can_node = self.can_network.add_node(node["node_id"], config["config_file"])
            can_node.nmt.wait_for_heartbeat()
            self.node_list.append(can_node)
            node_set[node["node_id"]] = {"transform": node["transform"], "obj": can_node, "active_cnt": 0}
        print("Check all nodes completed!")
        for node in self.node_list: 
            node.tpdo.read()
            node.tpdo[1].add_callback(self.proximity_callback)

    def proximity_callback(self, msg):
        node_id = msg.cob_id - 384
        for var in msg:
            self.gesture.update_prox(node_id, var.raw)

    def disconnect(self):
        self.can_network.disconnect()

def main():
    cs_canopen = CsCanOpen("can0", "./tw-island.toml")
    while True:
        time.sleep(1)
    return

if __name__ == "__main__":
    main()
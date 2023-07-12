#!/usr/bin/python3
#sudo ifconfig can0 txqueuelen 10000
#sudo ip link set can0 up type can bitrate 1000000
#git:https://github.com/CityScience-TaipeiTech/cityscope-canopen-controller
import tomli
import time
import canopen
import socketio

import typing

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

class CsCanOpen:
    def __init__(self, can_interface, config_file):
        self.config = self.load_config(config_file)
        self.can_network = self.canopen_init(can_interface)
        self.light_can_network = self.light_canopen_init(can_interface)
        self.prox_nodes = self.load_nodes(self.config["proximity"])
        self.light_node = self.load_light_nodes()
        self.prox_detect = []
        self.prox_active = []
        self.prox_left = {"node_id": 10, "distance": 300}
        self.prox_right = {"node_id": 11, "distance": 300}
        self.timer = None
        self.toward_direction = None
        self.MODE = "LOOP" # default
        self.prox_dict = {'right': 0, 'left': 0}        
        self.is_partial_light = False

    def load_config(self, config_file):
        with open(config_file, "rb") as f:
            toml_dict = tomli.load(f)
            return toml_dict

    def canopen_init(self, can_interface="can0"):
        network = canopen.Network()
        network.connect(channel=can_interface, bustype='socketcan')

        return network
    
    def light_canopen_init(self, can_interface="can0"):
        light_network = canopen.Network()
        light_network.connect(channel=can_interface, bustype='socketcan')

        return light_network
    
    def load_nodes(self, config):
        for node in config["nodes"]:            
            can_node = self.can_network.add_node(node["node_id"], config["config_file"])
            can_node.tpdo.read()
            can_node.tpdo[1].add_callback(self.proximity_callback)            
            node["RemoteNode"] = can_node

            print(node["node_id"])

    def load_light_nodes(self, config: typing.Optional[typing.Any] = None):
        global light_node
        light_node = self.light_can_network.add_node(83, 'DS301_profile_mcu.eds')        
        light_node.rpdo.read()   
        light_node.rpdo[1][0x6001].phys = 0x0f     
        light_node.rpdo[1].start(1.0)
        # light_node.rpdo[1].add_callback(self.proximity_callback)            
        # node["RemoteNode"] = can_node
        # print(node["node_id"])
        #light_node.rpdo[1][0x6001].phys = 0x00 # value can be any except 0
        #light_node.rpdo[1].start(0.1)
        print('light node', light_node)

    def proximity_callback(self, msg):
        node_id = msg.cob_id - 384
        for var in msg:
            if node_id == 11:                
                self.prox_right = {"node_id": node_id, "distance": var.raw}    
                
                if var.raw < 20:
                    self.prox_dict['right'] = 1

            elif node_id == 10:
                self.prox_left = {"node_id": node_id, "distance": var.raw}     

                if var.raw < 20:
                    self.prox_dict['left'] = 1                                            
            
        # self.prox_active    

    @sio.event
    def swap_event_watcher(self):
        while True:            

            if self.prox_dict['right'] == 1 and self.prox_dict['left'] == 1:
                # light_node.rpdo[1][0x6001].phys = 0x00
                # light_node.rpdo[1].start(0.1)
                # light_node.nmt.state = 'OPERATIONAL'
                self.prox_dict['right'] = 0
                self.prox_dict['left'] = 0

            if self.prox_dict['left'] == 1:
                sio.emit('GESTURE', 'SWAP_LEFT')                
                light_node.rpdo[1][0x6001].phys = 0x01 # value can be any except 0
                print('swap left')
                self.prox_dict['left'] = 0
                self.is_partial_light = True

            if self.prox_dict['right'] == 1:
                sio.emit('GESTURE', 'SWAP_RIGHT')
                # light_node.nmt.state = 'PRE-OPERATIONAL'                
                light_node.rpdo[1][0x6001].phys = 0x01 # value can be any except 0
                print('swap right')
                self.prox_dict['right'] = 0
                self.is_partial_light = True
            
            time.sleep(2)        
            light_node.rpdo[1][0x6001].phys = 0x00 # value can be any except 0
    
    def disconnect(self):
        self.can_network.disconnect()

        self.light_node.rpdo[1].stop()
    

def main():    
    try:
        # sio.connect('http://127.0.0.1:5010')
        sio.connect('ws://10.100.1.51:5010')
        cs_canopen = CsCanOpen("can0", "./tw-island-dev.toml")
        cs_canopen.swap_event_watcher()    
    finally:
        pass
        # cs_canopen.disconnect


if __name__ == "__main__":
    main()
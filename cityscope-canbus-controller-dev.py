#!/usr/bin/python3
#sudo ifconfig can0 txqueuelen 10000
#sudo ip link set can0 up type can bitrate 1000000
#git:https://github.com/CityScience-TaipeiTech/cityscope-canopen-controller
#i will add some fuc later
import tomli
import time
import canopen
import socketio

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
        self.prox_nodes = self.load_nodes(self.config["proximity"])
        self.prox_detect = []
        self.prox_active = []
        self.prox_left = {"node_id": 10, "distance": 300}
        self.prox_right = {"node_id": 11, "distance": 300}
        self.timer = None
        self.toward_direction = None
        self.MODE = "LOOP" # default
        self.prox_dict = {'right': 0, 'left': 0}

    def load_config(self, config_file):
        with open(config_file, "rb") as f:
            toml_dict = tomli.load(f)
            return toml_dict

    def canopen_init(self, can_interface="can0"):
        network = canopen.Network()
        network.connect(channel=can_interface, bustype='socketcan')
        return network
    
    def load_nodes(self, config):
        for node in config["nodes"]:
            print(node)
            can_node = self.can_network.add_node(node["node_id"], config["config_file"])
            can_node.tpdo.read()
            can_node.tpdo[1].add_callback(self.proximity_callback)            
            node["RemoteNode"] = can_node

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
                self.prox_dict['right'] = 0
                self.prox_dict['left'] = 0

            if self.prox_dict['left'] == 1:
                sio.emit('GESTURE', 'SWAP_LEFT')
                print('swap left')
                self.prox_dict['left'] = 0

            if self.prox_dict['right'] == 1:
                sio.emit('GESTURE', 'SWAP_RIGHT')
                print('swap right')
                self.prox_dict['right'] = 0
            
            time.sleep(0.5)        
    
    def disconnect(self):
        self.can_network.disconnect()

def main():    
    # sio.connect('http://127.0.0.1:5010')
    sio.connect('ws://10.100.1.51:5010')
    cs_canopen = CsCanOpen("can0", "./tw-island-dev.toml")
    cs_canopen.swap_event_watcher()
    
    # while True:
    #     time.sleep(1)
    # return

if __name__ == "__main__":
    main()
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
        if node_id not in self.prox_active:
            pass
        for var in msg:            
            print(str(node_id)+' : %s = %d cm' % (var.name, var.raw))

            # if var.raw > 20: 
            #     continue

            # now right is 11, left is 10
            # no interuppt is usually 200 cm
            if node_id == 11:                
                self.prox_right = {"node_id": node_id, "distance": var.raw}                            

            elif node_id == 10:
                self.prox_left = {"node_id": node_id, "distance": var.raw}                                
            
        # self.prox_active

    @sio.event
    def swap_event_watcher(self):
        while True:
            current_time = time.time()

            # pass the scene someone close to two sensors at one time
            if self.prox_right["distance"] and self.prox_left["distance"] <= 20:
                continue
            
            # if more five sec there no new prox then reset the timer
            if self.timer and current_time - self.timer > 5:
                self.timer = None
                self.toward_direction = None
                sio.emit("GESTURE", "LOOP_PLAY")

            # swap event condition is activated
            if self.timer:
                if self.toward_direction == "LEFT" and self.prox_left["distance"] <= 20:                    
                    sio.emit("GESTURE", "SWAP_LEFT")

                elif self.toward_direction == "RIGHT" and self.prox_right["distance"] <= 20:
                    sio.emit("GESTURE", "SWAP_RIGHT")

            if self.prox_right["distance"] <= 20:
                self.timer = time.time()                
                self.toward_direction = "LEFT"

            elif self.prox_left["distance"] <= 20:
                self.timer = time.time()
                self.toward_direction = "RIGHT"
    
    def disconnect(self):
        self.can_network.disconnect()

def main():    
    sio.connect('http://127.0.0.1:2567')
    cs_canopen = CsCanOpen("can0", "./tw-island-dev.toml")
    cs_canopen.swap_event_watcher()
    
    # while True:
    #     time.sleep(1)
    # return

if __name__ == "__main__":
    main()
#!/usr/bin/python3
import tomli
import time
import canopen
from fastapi import FastAPI
from fastapi_socketio import SocketManager

app = FastAPI()
sio = SocketManager(app=app)

@app.sio.on('join')
async def handle_join(sid, *args, **kwargs):
    await sio.emit('lobby', 'User joined')

@sio.on('test')
async def test(sid, *args, **kwargs):
    await sio.emit('hey', 'joe')

class CsCanOpen:
    def __init__(self, can_interface, config_file):
        self.config = self.load_config(config_file)
        self.can_network = self.canopen_init(can_interface)
        self.prox_nodes = self.load_nodes(self.config["proximity"])
        self.prox_active = []

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
            # print('%s = %d cm' % (var.name, var.raw, ))
            if var.raw > 50: continue
        self.prox_active
        
    def disconnect(self):
        self.can_network.disconnect()

cs_canopen = CsCanOpen("can0", "../tw-island.toml")

@app.get("/home")
async def root():
    msg = 124
    futures = [cs_canopen.proximity_callback()]
    a = await asyncio.gather(*futures)

    await asyncio.sleep(1)

    # return {'a': 'hello world'}
    return "Hello World"

@app.get("/cityscope")
async def cityscope():

    return "cityscope"

def main():
    # cs_canopen = CsCanOpen("can0", "../tw-island.toml")
    # while True:
    #     time.sleep(1)
    #     cs_canopen.proximity_callback
    # return

    # launch socketio server
    import logging
    import sys

    # logging.basicConfig(level=logging.DEBUG,
    #                     stream=sys.stdout)

    import uvicorn
    uvicorn.run("cityscope-canbus-controller:app", host='0.0.0.0', port=8000, reload=True)

if __name__ == "__main__":
    main()

    
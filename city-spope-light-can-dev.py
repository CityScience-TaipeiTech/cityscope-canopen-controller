#!/usr/bin/python3
# sudo ifconfig can0 txqueuelen 10000
# sudo ip link set can0 up type can bitrate 1000000
import tomli
import time
import canopen
import typing

class CsCanOpenNetwork:
    def __init__(self, can_interface, config_file: typing.Optional[typing.AnyStr] = None):
        if config_file is not None: self.config = self.load_config(config_file) 
        self.can_network = self.canopen_init(can_interface)
        pass

    def load_config(self, config_file: typing.AnyStr) -> typing.Dict:
        with open(config_file, 'rb') as f:
            toml_dict = tomli.load(f)
            return toml_dict
        
    def canopen_init(self, can_interface='can0'):
        network = canopen.Network()
        network.connect(channel=can_interface, bustype='socketcan')
        return network
    
    def load_nodes(self, config):
        # for node in config['node']:
        #     print(node)
        node = self.can_network.add_node(25, 'DS301_profile_mcu.eds')
        node.rpdo.read()
        node.nmt.state = 'PRE-OPERATIONAL'
        # print(node.rpdo.len())
        node.rpdo[1][0x6001].phys = 0x01
        node.rpdo[1].start(0.1)
        node.nmt.state = 'OPERATIONAL'
        time.sleep(2)
        node.rpdo[1][0x6001].phys = 0x00
        time.sleep(2)
        node.rpdo[1].stop()

def main() -> typing.NoReturn:
    cs_canopen = CsCanOpenNetwork('can0')

if __name__ == '__main__':
    main()

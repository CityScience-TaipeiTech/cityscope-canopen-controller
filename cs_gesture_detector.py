import time
from threading import Thread
from circular_queue import CircularQueue

class CsGestureDetector():
    def __init__(self, gesrure_config, proximity_config, buffer_size = 200):
        self.buffer_size = buffer_size
        self.config = gesrure_config
        self.node_dict = self.nodeset_init(proximity_config)
        self.event_timer = Thread(target=self.event_timer_callback)
        self.event_timer.start()
        self.control_node = -1

    def nodeset_init(self, proximity_config):
        node_dict = {}
        for node in proximity_config["nodes"]:
            node_dict[node["node_id"]] = {"transform": node["transform"], "queue": CircularQueue(self.buffer_size)}
        return node_dict

    def update_prox(self, node_id, distance):
        self.node_dict[node_id]["queue"].enqueue(distance)
    
    def get_control_node(self):
        active_counts = []
        active_counts_node = []
        for node_id, data in self.node_dict.items():
            # print("{}: {}".format(node_id, data))
            num_active_dis = 0
            for dis in data["queue"]:
                if dis < self.config["active_dis"]:
                    num_active_dis += 1
            active_counts.append(num_active_dis)
            active_counts_node.append(node_id)
        max_count = max(active_counts)
        max_index = active_counts.index(max_count)
        if max_count > 60:
            return active_counts_node[max_index]
        else:
            return -1

    
    def event_timer_callback(self):
        while True:
            self.control_node = self.get_control_node()
            time.sleep(0.1)
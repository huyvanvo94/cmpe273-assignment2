from hashlib import md5
from bisect import bisect


class Ring(object):

    def __init__(self, server_list, num_replicas=3):
        nodes = self.generate_nodes(server_list, num_replicas)
        hnodes = [self.hash(node) for node in nodes]
        hnodes.sort()

        self.num_replicas = num_replicas
        self.nodes = nodes
        self.hnodes = hnodes
        self.nodes_map = {self.hash(node): node.split("-")[1] for node in nodes}

    @staticmethod
    def hash(val):
        val = val.encode('utf-8')
        m = md5(val)
        return int(m.hexdigest(), 16)

    @staticmethod
    def generate_nodes(server_list, num_replicas):
        nodes = []
        for i in range(num_replicas):
            for server in server_list:
                nodes.append("{0}-{1}".format(i, server))
        return nodes

    def get_node(self, val):
        pos = bisect(self.hnodes, self.hash(val))
        if pos == len(self.hnodes):
            return self.nodes_map[self.hnodes[0]]
        else:
            return self.nodes_map[self.hnodes[pos]]


server_list = ["127.0.0.1", "127.0.0.2", "127.0.0.3"]
ring = Ring(server_list)
print(ring.get_node("KNKLn"))
print(ring.get_node("12213"))
print(ring.get_node("2434"))
print(ring.get_node("1"))
from utils import *


class Node(object):
    def __init__(self, object):
        self.object = object

    def __str__(self):
        return str(self.object)

    def __repr__(self):
        return self.__str__()

    def getKey(self):
        return self.object

class VirtualNode(object):

    def __init__(self, physicalNode, replicaIndex):
        self.physicalNode = physicalNode
        self.replicaIndex = replicaIndex

    def isVirtualNodeOf(self, pNode):
        return self.physicalNode.getKey() == pNode.getKey()

    def getKey(self):
        return "{}-{}".format(self.physicalNode.getKey(), self.replicaIndex)

    def __str__(self):
        return self.getKey()

    def __repr__(self):
        return self.__str__()

    def getPhysicalNode(self):
        return self.physicalNode

class ConsistentHashRouter(object):
    def __init__(self, pNodes, vNodeCount, hash, pNodeIsString=True):
        self.hash = hash
        self.ring = dict()

        if pNodeIsString:
            for pNode in pNodes:
                self.addNode(Node(pNode), vNodeCount)
        else:
            for pNode in pNodes:
                self.addNode(pNode, vNodeCount)

    def addNode(self, pNode, vNodeCount):

        existingReplicas = self.getExistingReplicas(pNode)

        for i in range(vNodeCount):
            vNode = VirtualNode(pNode, i + existingReplicas)

            self.ring[self.hash(vNode.getKey())] = vNode

    def removeNode(self, pNode):

        for key in self.ring.keys():
            virtualNode = self.ring.get(key)

            if virtualNode.isVirtualNodeOf(pNode):
                del self.ring[key]


    def routeNode(self, objectKey):

        if len(self.ring) == 0:
            return None
        mkeys = sorted(list(self.ring.keys()))
        hashVal = self.hash(objectKey)

        pos = self._find(mkeys, hashVal)

        if pos == len(mkeys):
            return self.ring[mkeys[0]]
        else:
            return self.ring[mkeys[pos]]

    def select(self, objectKey):
        return self.routeNode(objectKey).getPhysicalNode().getKey()

    def getExistingReplicas(self, pNode):
        replicas = 0

        for vNode in self.ring.values():
            if vNode.isVirtualNodeOf(pNode):
                replicas = replicas + 1

        return replicas

    def _find(self, lst, x):
        lo = 0
        hi = len(lst)

        while lo < hi:
            mid = (lo + hi) // 2
            if lst[mid] < x:
                lo = mid + 1

            else:
                hi = mid

        return lo

from bisect import bisect


class Ring(object):

    def __init__(self, server_list, num_replicas=2):
        nodes = self.generate_nodes(server_list, num_replicas)
        hnodes = [self.hash(node) for node in nodes]
        hnodes.sort()

        self.num_replicas = num_replicas
        self.nodes = nodes
        self.hnodes = hnodes
        self.nodes_map = {self.hash(node): node for node in nodes}
      #   self.nodes_map = {self.hash(node): node.split("-")[1] for node in nodes}

    @staticmethod
    def hash(val):
        m = md5(val)
        return m

    @staticmethod
    def generate_nodes(server_list, num_replicas):
        nodes = []
        for i in range(num_replicas):
            for server in server_list:
                nodes.append("{0}-{1}".format(server, i))
        return nodes

    def get_node(self, val):

        print(self.nodes_map)

        pos = bisect(self.hnodes, self.hash(val))
        print(pos)

        if pos == len(self.hnodes):

            return self.nodes_map[self.hnodes[0]]
        else:
            return self.nodes_map[self.hnodes[pos]]






def my_bisection(lst, x):

    lo = 0
    hi = len(lst)

    while lo < hi:
        mid = (lo + hi)//2
        if lst[mid] < x:
            lo = mid + 1

        else:
            hi = mid

    return lo

def find(lst, x):

    i = 0

    while i < len(lst):

        if lst[i] >= x: break
        i += 1

    return i

lst = [1,2,3,4,5]
print(find(lst, 3.1))

print(my_bisection(lst, 3.1 ))


servers = ['a', 'b', 'c']
r = Ring(servers)
nodes = [Node(server) for server in servers]

print(nodes)



ch = ConsistentHashRouter(servers, 2, md5)


print(ch.ring)

s = "fvfffdfsdfhdfh"

print("yes: ", ch.select(s))


print("no: ", r.get_node(s))
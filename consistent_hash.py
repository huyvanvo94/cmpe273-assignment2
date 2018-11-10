import sys
import csv
from utils import *
from csv_paser import  *
import requests
from servers import servers


class ConsistentHash(object):
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

cHash = ConsistentHash(pNodes=servers, vNodeCount=10, hash=md5, pNodeIsString=True )

def main(filename):

    csv_reader = read_csv(filename)

    for row in csv_reader:
        try:
            xxxx = pretty_csv_row(csv_reader, row)

            server = cHash.select(xxxx)
            json = {
                "xxxx": xxxx
            }

            url = server + '/api/v1/entries'

        #    print(url)

            requests.post(url=url, data=json)
        except:
            print('something went wrong')
            pass




if __name__== '__main__':


    filename = 'causes-of-death.csv'

    if len(sys.argv) > 1:
        filename = str(sys.argv[1])

    row_count = sum(1 for row in read_csv(filename))

    print("Uploaded all {} entries.".format(row_count))

    print("Verifying the data.")

    main(filename)





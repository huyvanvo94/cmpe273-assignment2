
import hashlib
import bisect
from collections import defaultdict
import binascii
import time
import math
from functools import wraps

class CollisionError(Exception):
    pass


_collisions = {}



def catch_collision(func):
    @wraps(func)
    def _catch(key):
        res = func(key)
        if res in _collisions and key != _collisions[res]:
            raise CollisionError('%s and %s with %s' % (key, _collisions[res],
                func))
        _collisions[res] = key
        return res
    return _catch

@catch_collision
def fnv32a(key):
    hval = 0x811c9dc5
    fnv_32_prime = 0x01000193
    uint32_max = 2 ** 32
    for s in key:
        hval = hval ^ ord(s)
        hval = (hval * fnv_32_prime) % uint32_max
    return hval


@catch_collision
def sha512(key):
    return int(hashlib.sha512(key).hexdigest(), 16)


@catch_collision
def sha256(key):
    key = key.encode('utf-8')
    return int(hashlib.sha256(key).hexdigest(), 16)


@catch_collision
def md5(key):
    key = key.encode('utf-8')
    return int(hashlib.md5(key).hexdigest(), 16)


class ConsistentHash:

    def __init__(self, nodes=None,replicas=1, hash=md5):
        if nodes is None:
            nodes = []
        self.nodes = nodes
        self.replicas = replicas
        self.hash = hash
        self.rings = dict()
        self.replicasNodes = []
        for node in self.nodes:
            self.computeRings(node)


    def computeRings(self, node):
        for count in range( self.replicas):
            replicated = str(node) + '-'+str(count+1)
            self.replicasNodes.append(replicated)
            h = self.hash(replicated) % (2*math.pi)
            self.rings[replicated] = h

    def add(self, node):
        self.nodes.append(node)
        self.computeRings(node)

    def remove(self, node):
        self.nodes.remove(node)

        for count in range(self.replicas):
            replicated = str(node) + '-'+str(count+1)

            self.replicasNodes.remove(replicated)
            del self.rings[replicated]

    def get(self, key):

        h = self.hash(key) % (2*math.pi)


        theNode = None
        diff = None

        for node in self.replicasNodes:
            if h < self.rings[node]:

                nDf = self.rings[node] - h

                if diff is None:
                    diff = nDf
                    theNode = node
                else:

                    if nDf < diff:
                        diff = nDf
                        theNode = node


        if theNode is None:
            return self.replicasNodes[0].split('-')[0]

        return theNode.split('-')[0]





def makeServers(n):
    servers = []
    for j in range(n):

        servers.append('server'+str(j))

    return servers

N = 4
T = 15

servers = makeServers(N)

ch = ConsistentHash(nodes=makeServers(N))

testKeys = ['akey'+str(i) for i in range(T)]


def test():
    lst = []

    for key in testKeys:
        server = ch.get(key)

        lst.append(server)
    return lst

l1 = test()

print(l1)

ch.remove('server1')

l2 = test()

print(l2)


count = 0

for i in range(len(l2)):

    if l1[i] != l2[i]:
        count += 1

print(count)

def _repl(name, index):
    return '%s:%d' % (name, index)


class ConsistentHashing(object):

    def __init__(self, ips=[], replicas=200, hash=md5):
        self._ips = {}
        self._hashed_ips = []
        self.replicas = replicas
        self._hash = hash

        for ip in ips:
            self.add(ip)

    def __str__(self):
        return '<ConsistentHashing with %s hash>' % self._hash

    def add(self, ip):
        for i in range(self.replicas):
            sip = _repl(ip, i)
            hashed = self._hash(sip)
            self._ips[hashed] = sip
            bisect.insort(self._hashed_ips, hashed)

    def remove(self, ip):
        for i in range(self.replicas):
            sip = _repl(ip, i)
            hashed = self._hash(sip)
            del self._ips[hashed]
            index = bisect.bisect_left(self._hashed_ips, hashed)
            del self._hashed_ips[index]

    def select(self, username):
        hashed = self._hash(username)
        start = bisect.bisect(self._hashed_ips, hashed,
                              hi=len(self._hashed_ips)-1)
        return self._ips[self._hashed_ips[start]].split(':')[0]

ching = ConsistentHashing(ips=makeServers(N))

def tester():
    lst = []

    for key in testKeys:
        server = ching.select(key)

        lst.append(server)
    return lst


l22 = tester()

print(l22)

ching.remove('server1')

lww = tester()
print(lww)
p = 0
for i in range(len(lww)):

    if lww[i] != l22[i]:
        p += 1

print(p)
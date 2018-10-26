# https://ziade.org/2016/05/16/consistent-load-balancing/


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import bisect
from collections import defaultdict
import binascii
import time
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
    return int(hashlib.md5(key).hexdigest(), 16)


def hash(key):
    key = key.encode('utf-8')
    return int(hashlib.md5(key).hexdigest(), 16)



class RendezVousHash:

    def __init__(self, nodes=None, hashFunction=hash):
        if nodes is None:
            nodes = []

        self.nodes = nodes
        self.hashFunction = hashFunction




    def getNode(self, key):

        theMax = self.hashFunction(str(self.nodes[0])+str(key))

        theNode = self.nodes[0]

        for idx in range(1, len(self.nodes)):

            tempMax = self.hashFunction(str(self.nodes[idx] + str(key)))

            if tempMax > theMax:

                theMax = tempMax
                theNode = self.nodes[idx]
        return theNode


    def remove(self, node):

        self.nodes.remove(node)
    def add(self, node):
        self.nodes.append(node)



if __name__ == '__main__':
    servers = [
        'server1',
        'server2',
        'server3',
        'server4',
        'server5'
    ]

    ch = RendezVousHash(nodes=servers, hashFunction=sha256)


    testKeys = [
        '123',
        '1231412',
        '324235252',
        '23423423',
        '435345353'
    ]

    for key in testKeys:
        server = ch.getNode(key)

        print('the key: {} the server: {}'.format(key, server))

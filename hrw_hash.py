#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import bisect
from collections import defaultdict
import binascii
import time
from functools import wraps
from utils import *
import requests
from csv_paser import *
import sys
from servers import *

class RendezVousHash(object):

    def __init__(self, nodes=None, hashFunction=md5):
        if nodes is None:
            nodes = []

        self.nodes = nodes
        self.hashFunction = hashFunction

    def select(self, key):
        idx = 0
        maxweight = self.hashFunction("%s-%s" % (str(self.nodes[idx]), str(key)))

        for i in range(1, len(self.nodes)):

            weight = self.hashFunction("%s-%s" % (str(self.nodes[i]), str(key)))

            if weight > maxweight:
                maxweight = weight
                idx = i
            elif weight == maxweight:
                maxweight = weight

                maxs = max(str(self.nodes[i]), str( self.nodes[idx]) )

                if maxs == str(self.nodes[i]):
                    idx = i


        return self.nodes[idx]



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

class TRendezVous(object):

    def __init__(self, ips=None, hash=md5):
        if ips is None:
            ips = []
        self.ips = ips
        self._hash = hash

    def __str__(self):
        return '<RendezVous with %s hash>' % self._hash

    def add(self, ip):
        self.ips.append(ip)

    def remove(self, ip):
        self.ips.remove(ip)

    def select(self, key):
        high_score = -1
        winner = None
        for ip in self.ips:
            score = self._hash("%s-%s" % (str(ip), str(key)))
            if score > high_score:
                high_score, winner = score, ip

            elif score == high_score:
                high_score, winner = score, max(str(ip), str(winner))
        return winner


rHash = RendezVousHash(nodes=servers)


def main(filename):

    csv_reader = read_csv(filename)

    for row in csv_reader:
        try:
            xxxx = pretty_csv_row(csv_reader, row)

            server = rHash.getNode(xxxx)

            url = server + '/api/v1/entries'

            requests.post(url=url, data={"xxxx": xxxx})
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
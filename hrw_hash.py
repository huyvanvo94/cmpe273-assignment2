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

from servers import *

class RendezVousHash:

    def __init__(self, nodes=None, hashFunction=md5):
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

rHash = RendezVousHash(nodes=servers)
def main(filename):

    csv_reader = read_csv(filename)

    for row in csv_reader:
        try:
            xxxx = pretty_csv_row(csv_reader, row)

            server = rHash.getNode(xxxx)
            json = {
                "xxxx": xxxx
            }
            params = {'format': 'json', "Content-Type": "application/json"}
          #  print('post server {} with json {}'.format(server, json))

          #  url = 'http://localhost:5000' + '/api/v1/entries'
            url = server + '/api/v1/entries'
            print('to {}'.format(url))
            requests.post(url="http://localhost:5000/api/v1/entries", data=json)
        except:
            print('something went wrong')
            pass

if __name__== '__main__':


    filename = 'causes-of-death.csv'
    main(filename)
  #  requests.post(url="http://localhost:5000/api/v1/entries", data={'xxxx': 'tester'})

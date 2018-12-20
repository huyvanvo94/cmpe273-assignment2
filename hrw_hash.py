#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *
import requests
from csv_paser import *
import sys
from servers import *

# rendezvous hash algorithm
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

# end rendezvous hash algorithm

rHash = RendezVousHash(nodes=servers)

# function to read csv and do work
def main(filename):

    csv_reader = read_csv(filename)

    for row in csv_reader:
        try:
            xxxx = pretty_csv_row(csv_reader, row)

            server = rHash.getNode(xxxx)

            url = server + '/api/v1/entries'
            try:
                requests.post(url=url, data={"xxxx": xxxx})
            except: pass
        except:
            print('something went wrong')
            pass

    # save output to txt file
    # clear txt file
    open('hrw_hash_output.txt', 'w').close()

    row_count = sum(1 for row in read_csv(filename))
    with open('hrw_hash_output.txt', 'a') as f:
        f.write("Uploaded all {} entries.".format(row_count) + '\n')
        f.write("Verifying the data.\n")
    log_hrw_hash()




if __name__== '__main__':
    filename = 'consis'

    if len(sys.argv) > 1:
        filename = str(sys.argv[1])

    row_count = sum(1 for row in read_csv(filename))
    print("Uploaded all {} entries.".format(row_count))
    print("Verifying the data.")

    main(filename)
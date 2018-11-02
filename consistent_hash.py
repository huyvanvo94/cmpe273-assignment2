import sys
import csv
from utils import *
from csv_paser import  *
import requests
from servers import servers

def _repl(name, index):
    return '%s!%d' % (name, index)


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
        return self._ips[self._hashed_ips[start]].split('!')[0]

cHash = ConsistentHashing(ips=servers)

def main(filename):

    csv_reader = read_csv(filename)

    for row in csv_reader:
        try:
            xxxx = pretty_csv_row(csv_reader, row)

            server = cHash.select(xxxx)
            json = {
                "xxxx": xxxx
            }
            params = {'format': 'json', "Content-Type": "application/json"}
          #  print('post server {} with json {}'.format(server, json))

          #  url = 'http://localhost:5000' + '/api/v1/entries'
            url = server + '/api/v1/entries'
            print('to {}'.format(url))
            requests.post(url=url, data=json)
        except:
            print('something went wrong')
            pass




if __name__== '__main__':


    filename = 'causes-of-death.csv'

    main(filename)





import hashlib
import requests
from functools import wraps
import json
"""
Basic utils functions 
"""
DEBUG = True

class CollisionError(Exception):
    pass

def log_getrequest(url, filename):

    try:
        with open(filename, 'a') as f:

            r = requests.get(url=url)
            content = r.json()

            print('GET {}\n'.format(url))

            pretty_content = json.dumps(content, indent=2)
            print(pretty_content)
            f.write('GET {}\n'.format(url))
            f.write(pretty_content)

    except:
        pass



_collisions = {}

def convert(func):
    def utf8(args):

        args = args.encode('utf-8')

        func(args)

    return utf8

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
def md5(key):
    key = key.encode('utf-8')
    return int(hashlib.md5(key).hexdigest(), 16)

urls = ['http://localhost:5000/api/v1/entries', 'http://localhost:5001/api/v1/entries', 'http://localhost:5002/api/v1/entries', 'http://localhost:5003/api/v1/entries']

def log_hrw_hash():
    # clear txt file
    # open('hrw_hash_output.txt', 'w').close()
    for url in urls:
        log_getrequest(url, 'hrw_hash_output.txt')

def log_consistent_hash():
    # open('consistent_hash_output.txt', 'w').close()
    for url in urls:
        log_getrequest(url, 'consistent_hash_output.txt')





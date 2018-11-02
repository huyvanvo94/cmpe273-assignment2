import hashlib
import bisect
from collections import defaultdict
import binascii
import time
from functools import wraps

class CollisionError(Exception):
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

@convert
@catch_collision
def fnv32a(key):
    hval = 0x811c9dc5
    fnv_32_prime = 0x01000193
    uint32_max = 2 ** 32
    for s in key:
        hval = hval ^ ord(s)
        hval = (hval * fnv_32_prime) % uint32_max
    return hval

@convert
@catch_collision
def sha512(key):
    return int(hashlib.sha512(key).hexdigest(), 16)

@convert
@catch_collision
def sha256(key):
    key = key.encode('utf-8')
    return int(hashlib.sha256(key).hexdigest(), 16)


@catch_collision
def md5(key):
    key = key.encode('utf-8')
    return int(hashlib.md5(key).hexdigest(), 16)
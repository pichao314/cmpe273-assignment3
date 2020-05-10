import mmh3
from bitarray import bitarray
from math import log
from functools import partial


class BloomFilter:
    # figure the bit size and hash func size, initialize the bit array with 0
    def __init__(self, n, fp):
        self.BIT_SIZE = int(- (n * log(fp)) / log(2) ** 2)
        self.HASH_NUM = int((self.BIT_SIZE / n) * log(2))
        self.bit_array = bitarray(self.BIT_SIZE)
        self.bit_array.setall(0)

    # add a key by setting all relative bit into 1
    def add(self, key):
        point_list = self.get_positions(key)
        for b in point_list:
            self.bit_array[b] = 1

    # check if the key is a member
    def is_member(self, url):
        point_list = self.get_positions(url)
        result = True
        for b in point_list:
            result = result and self.bit_array[b]
        return result

    # get the positive bits of a key
    def get_positions(self, key):
        return [hf(key) % self.BIT_SIZE for hf in [partial(mmh3.hash, seed=s) for s in range(self.HASH_NUM)]]

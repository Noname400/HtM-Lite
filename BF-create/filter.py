from math import ceil, log
from mmh3 import hash
from struct import pack, unpack, calcsize
from bitarray import bitarray


class BloomFilter(object):
    def __init__(self, size, fp_probability=1e-12):
        self.__used_size = 0
        self.__size = size
        self.__fp_probability = fp_probability

        if self.__size:
            self.__filter_size = ceil(
                -self.__size*log(self.__fp_probability)/log(2)**2
            )

            self.__num_hashes = round(
                self.__filter_size * log(2) / self.__size)

            self.__filter = bitarray(self.__filter_size, endian='little')
            self.__filter.setall(False)
        else:
            self.__filter = bitarray(endian='little')

    @classmethod
    def load(cls, fp, n=-1):
        header = '<dQQQQ'
        header_size = calcsize(header)
        fp_prob, used_size, size, filter_size, num_hashes = unpack(
            header,
            fp.read(header_size)
        )
        bloom_filter = cls(size=0, fp_probability=fp_prob)
        if n >= header_size:
            bloom_filter.__filter.frombytes(fp.read(n - header_size))
        else:
            bloom_filter.__filter.frombytes(fp.read())
        assert len(bloom_filter.__filter) == filter_size or len(bloom_filter.__filter) == filter_size + (
            8 - filter_size % 8
        ), 'Bloom filter size mismatch!'

        bloom_filter.__used_size = used_size
        bloom_filter.__size = size
        bloom_filter.__filter_size = filter_size
        bloom_filter.__num_hashes = num_hashes
        return bloom_filter

    def save(self, fp):
        fp.write(
            pack(
                '<dQQQQ',
                self.__fp_probability,
                self.__used_size,
                self.__size,
                self.__filter_size,
                self.__num_hashes,
            )
        )

        fp.write(self.__filter.tobytes())

    @property
    def filter_size(self):
        return self.__filter_size

    @property
    def num_hashes(self):
        return self.__num_hashes

    @property
    def fp_prob(self):
        return self.__size

    @property
    def size(self):
        return self.__size

    def __len__(self):
        return self.__used_size

    def add(self, item):
        if item not in self and self.__used_size < self.__size:
            for i in range(self.__num_hashes):
                self.__filter[hash(item, i) % self.__filter_size] = True

            self.__used_size += 1

    def __contains__(self, item):
        for i in range(self.__num_hashes):
            if not self.__filter[hash(item, i) % self.__filter_size]:
                return False

        return True

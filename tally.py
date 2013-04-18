# just a script to count the number of zero and one bits in files
#
# example use:
#   find ~/src/ -name '*.py'| python tally.py
#   bittally: zeros v ones: 10925500 (58.1%) - 7894388 (41.9%)
import mmap
import sys

def count_ones(c):
    ones = 0
    while c:
        if c%2:
            ones += 1
        c = c >> 1
    return ones

def make_lookup_table():
    table = {}
    for i in range(256):
        table[chr(i)] = count_ones(i)
    return table

lookuptable = make_lookup_table()

def tally_file(filename):
    with open(filename) as f:
        ones = 0
        mm = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
        size = mm.size()
        for c in range(size):
            ones += lookuptable[mm.read_byte()]
    return (8*size-ones), ones


ones = 0
zeros = 0
for filename in sys.stdin:
    f = filename.strip()
    try:
        tally = tally_file(f)
        zeros += tally[0]
        ones += tally[1]
    except:
        pass

print "bittally: zeros v ones: %d (%.1f%%) - %d (%.1f%%)" % (zeros, 100.*zeros/(ones+zeros),
                                                             ones,  100.*ones/(ones+zeros))

__author__ = 'Or'
import random
import time
import socket
import struct
import bencode

l = [1,2,3,4,5,6]
p = bencode.bencode(l)
print p
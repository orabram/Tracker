__author__ = 'Or'
import random
import time
import socket
import struct

i = 3
i = struct.pack(">b", i)[0]
print struct.unpack(">b", i)[0]
print i
import pickle
import os
"""
f = open("C:\\Users\\Or\\Documents\\GitHub\\Tracker\\123.txt", "w")
f.write("45789")
f.write("516384")
pickle.dump({'aric': 1, 'beth': 2}, f)
f.close()
f = open("C:\\Users\\Or\\Documents\\GitHub\\Tracker\\123.txt", "r")
num = int(f.read(1))
port = f.read(num)
num = int(f.read(1))
buffer = f.read(num)
info = pickle.load(f)
print info
f.close()
f = open("C:\\Users\\Or\\Documents\\GitHub\\Tracker\\123.txt", "w")
f.write("45789")
f.write("516384")
pickle.dump({'erica': 3, 'beth': 4}, f)
f.close()"""
f = open("C:\\Users\\Or\\Documents\\GitHub\\Tracker\\123.txt", "w")
files = {'erica': 3, 'beth': 4}
port = 5789
buffer = 16384
print port.bit_length()
f.write(str(len(str(port))))
f.write(str(port))
f.write(str(len(str(buffer))))
f.write(str(buffer))
pickle.dump(files, f)
f.close()
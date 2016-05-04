import pickle

file = open("C:\\settings\\settings.dat", "r")
num = int(file.read(1))
port = file.read(num)
if port == "":
    port = 5789
port = int(port)
num = int(file.read(1))
buffer = file.read(num)  # The largest piece size I'm allowing is 4000000 bytes.
if buffer == "":
    buffer = 16384
buffer = int(buffer)
files = pickle.load(file)
if files == "":
    files = {}
print port
print buffer
print files

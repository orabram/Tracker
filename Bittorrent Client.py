import socket
from bencode import bdecode
import os

BUFFER = 4096

gui = socket.socket()
gui.connect(("127.0.0.1", 3467))
path = gui.recv(BUFFER)
f = open(path, 'rb')
content = open(path, 'rb').read()
dct = bdecode(content)
announce_url = dct['announce']
filename = dct['info']['name']
address = announce_url.split("//")
address = address[1]
ip = address.split(":")[0]
s = socket.socket()
s.connect((ip, 9876))
s.send(filename)
gui.send("downloading...")
file = ""
data = s.recv(BUFFER)
while data != "done":
    file += data
    data = s.recv(BUFFER)
s.close()
dir_name = filename.split(".")
true_dir_name = dir_name[0]
for i in dir_name[1:-1]:
    true_dir_name += "." + i
directory = "C:\\" + true_dir_name
if not os.path.exists(directory):
    os.makedirs(directory)
f = open("C:\\" + true_dir_name + "\\" + filename, "wb")
f.write(data)
gui.send("Completed successfully!")
__author__ = 'Or'
import struct
import socket
import os
from TrackerCommunicationManager import *

BUFFER = 4098
PTSR = "BitTorrent protocol"
PTSRLEN = len(PTSR)
KEEP_ALIVE = struct.pack(">i", 0)
CHOKE = struct.pack(">bb", 1, 0)
UNCHOKE = struct.pack(">bb", 1, 1)
INTERESTED = struct.pack(">bb", 1, 2)
NOT_INTERESTED = struct.pack(">bb", 1, 3)
HAVE = struct.pack(">bb", 5, 4)
#CHOKE = struct.pack(">ib", 1, struct.pack(">b", 0)[0])
#UNCHOKE = struct.pack(">ib", 1, struct.pack(">b", 1)[0])
#INTERESTED = struct.pack(">ib", 1, struct.pack(">b", 2)[0])
#NOT_INTERESTED = struct.pack(">ib", 1, struct.pack(">b", 3)[0])
#HAVE = struct.pack(">ib", 5, struct.pack(">b", 4)[0])
FILE_LOCATION = os.path.dirname(os.path.abspath(__file__)) + '\\Files\\Storage'

class ClientCommunication():
    def __init__(self, socket, tcm):
        self.socket = socket
        self.files = tcm.get_files() #contains the chunks of the file
        self.am_choking = True
        self.am_interested = False
        self.peer_choking = True
        self.peer_interested = False
        self.done = False

    def handshake(self):
        handshake = self.socket.recv(BUFFER)
        if len(handshake) < 49:
            self.socket.close()
        ptsrlen, ptsr = struct.unpack(">b19s", handshake[:20])[0]
        if ptsrlen == PTSRLEN and PTSR == ptsr:
            info_hash = struct.unpack(">20s", handshake[28:48][0])
            for file in self.files:
                if info_hash == self.files[file][3]:
                    self.socket.send(HAVE + struct.pack(">i", self.files[file][2]))
                    return file
            else:
                self.socket.close()
        else:
            self.socket.close()
        return False

    def send_requested_block(self, block_length, piece_num, index):
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abs_file_path = os.path.join(script_dir, FILE_LOCATION)
        f = open(abs_file_path, "rb+")
        f.seek(index)
        data = f.read(block_length)
        piece = struct.pack(">ibii" + str(block_length) + "s", (9 + block_length), struct.pack(">i", 7)[0], piece_num, index, data)
        self.socket.send(piece)

    def manage_download(self):
        self.socket.settimeout(2)
        file = self.handshake()
        if file != False:
            self.socket.send(UNCHOKE)
            self.am_choking = False
            while self.done == False:
                packet = self.socket.recv(BUFFER)
                id = struct.unpack(">b", packet[5])[0]
                if id == 6 and len(packet) == 13:
                    piece_num, index, length = struct.unpack(">iii", packet[5:12])[0]
                    if self.have_piece(file, piece_num):
                        self.send_requested_block(length, piece_num, index)
                elif id == 4 and len(packet) == 5:
                    piece_num = struct.unpack(">i", packet[4])[0]
                    if self.have_piece(file, piece_num):
                        self.done = True

    def have_piece(self, tfile, piece_num):
        for file in self.files:
            if file == tfile:
                if self.files[1] == piece_num:
                    return True
        return False






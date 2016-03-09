__author__ = 'Or'
import struct
import socket
import os
from TrackerCommunicationManager import *

BUFFER = 4098
PTSR = "BitTorrent protocol"
PTSRLEN = len(PTSR)
KEEP_ALIVE = struct.pack(">i", 0)
CHOKE = struct.pack(">ib", 1, struct.pack(">b", 0)[0])
UNCHOKE = struct.pack(">ib", 1, struct.pack(">b", 1)[0])
INTERESTED = struct.pack(">ib", 1, struct.pack(">b", 2)[0])
NOT_INTERESTED = struct.pack(">ib", 1, struct.pack(">b", 3)[0])
HAVE = struct.pack(">ib", 5, struct.pack(">b", 4)[0])
FILE_LOCATION = "ccc" # will be decided later

class ClientCommunication():
    def __init__(self, socket, file, info_hash, piece_length, piece_num):
        self.socket = socket
        self.file = file #contains the chunks of the file
        self.info_hash = info_hash #contains the info_hash of the file
        self.buffer = piece_length
        self.am_choking = True
        self.am_interested = False
        self.peer_choking = True
        self.peer_interested = False
        self.piece_num = piece_num
        self.piece_length = piece_length
        self.done = False

    def handshake(self):
        handshake = self.socket.recv(BUFFER)
        if len(handshake) < 49:
            self.socket.close()
        ptsrlen, ptsr = struct.unpack(">b19s", handshake[:20])
        if ptsrlen == PTSRLEN and PTSR == ptsr:
            info_hash = struct.unpack(">20s", handshake[28:48])
            if info_hash == self.info_hash:
                self.socket.send(HAVE + struct.pack(">i", self.piece_num))
            else:
                self.socket.close()
        else:
            self.socket.close()

    def send_requested_block(self, block_length, piece_num, index):
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abs_file_path = os.path.join(script_dir, FILE_LOCATION)
        f = open(abs_file_path, "rb")
        f.seek(index)
        data = f.read(block_length)
        piece = struct.pack(">ibii" + block_length + "s", (9 + block_length), struct.pack(">i", 7)[0], piece_num, index, data)
        self.socket.send(piece)

    def manage_download(self):
        self.socket.settimeout(2)
        self.handshake()
        self.socket.send(UNCHOKE)
        self.am_choking = False
        while self.done == False:
            packet = self.socket.recv(BUFFER)
            id = struct.unpack(">b", packet[5])[0]
            if id == 6 and len(packet) == 13:
                piece_num, index, length = struct.unpack(">iii", packet[5:12])[0]
                if piece_num == self.piece_num:
                    self.send_requested_block(length, piece_num, index)
            elif id == 4 and len(packet) == 5:
                piece_num = struct.unpack(">i", packet[4])[0]
                if piece_num == self.piece_num:
                    self.done = True







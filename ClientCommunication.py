__author__ = 'Or'
#region -------------Info------------
# Name: Client Communication Manager
# Version: 1.0
# By: Or Abramovich
#endregion -------------Info------------

#region -------------Imports---------
import struct
import socket
import os
from TrackerCommunicationManager import *

#endregion -------------Imports---------

#region -------------Constants--------------

BUFFER = 4098
PTSR = "BitTorrent protocol"
PTSRLEN = len(PTSR)
KEEP_ALIVE = struct.pack(">i", 0)
CHOKE = struct.pack(">1b1b", 1, 0)
UNCHOKE = struct.pack(">1b1b", 1, 1)
INTERESTED = struct.pack(">1b1b", 1, 2)
NOT_INTERESTED = struct.pack(">1b1b", 1, 3)
HAVE = struct.pack(">1b1b", 5, 4)
#CHOKE = struct.pack(">ib", 1, struct.pack(">b", 0)[0])
#UNCHOKE = struct.pack(">ib", 1, struct.pack(">b", 1)[0])
#INTERESTED = struct.pack(">ib", 1, struct.pack(">b", 2)[0])
#NOT_INTERESTED = struct.pack(">ib", 1, struct.pack(">b", 3)[0])
#HAVE = struct.pack(">ib", 5, struct.pack(">b", 4)[0])
FILE_LOCATION = os.path.dirname(os.path.abspath(__file__)) + '\\Files\\Storage'

#endregion -------------Constants--------------


class ClientCommunication():
    def __init__(self, socket, tcm):
        self.socket = socket
        self.files = tcm.get_files() #contains the chunks of the file
        self.am_choking = True
        self.am_interested = False
        self.peer_choking = True
        self.peer_interested = False
        self.done = False # These 5 parameters are the Initial state of the connection

    # Performs an handshake with the connecting client.
    def handshake(self):
        handshake = self.socket.recv(BUFFER)
        if len(handshake) < 49: # If the length isn't right, close the connection.
            self.socket.close()
        ptsrlen, ptsr = struct.unpack(">b19s", handshake[:20])[0] # Check if the values match
        if ptsrlen == PTSRLEN and PTSR == ptsr:
            info_hash = struct.unpack(">20s", handshake[28:48][0])
            for file in self.files: # Check if you currently have this file
                if info_hash == self.files[file][3]:
                    self.socket.send(HAVE + struct.pack(">i", self.files[file][2]))
                    return file # If you do, complete the handshake and return the file.
            else:
                self.socket.close() # If not, close the connection.
        else:
            self.socket.close()
        return False

    # Sends the requested piece.
    def send_requested_block(self, block_length, piece_num, index):
        script_dir = os.path.dirname(__file__)
        abs_file_path = os.path.join(script_dir, FILE_LOCATION)
        f = open(abs_file_path, "rb+")
        f.seek(index) # Open the file in the block's index
        data = f.read(block_length)
        piece = struct.pack(">ibii" + str(block_length) + "s", (9 + block_length), struct.pack(">i", 7)[0], piece_num, index, data) # Read it and send it, according to the protocol.
        self.socket.send(piece)

    # Manages the download for the client
    def manage_download(self):
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
        else:
            print "the file doesn't exist"

    # Checks if a file exists in the current machine
    def have_piece(self, tfile, piece_num):
        for file in self.files:
            if file == tfile:
                if self.files[1] == piece_num:
                    return True
        return False






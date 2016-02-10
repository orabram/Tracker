__author__ = 'Or'
import struct
import socket
import time
import random

BUFFER = 4096

class ClientManager():
    def __init__(self, ip, port):
        self.interval = 120
        self.files = {}
        self.downloaders = {}
        self.ip = ip
        self.port = port

    def wait_for_connections(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((self.ip, self.port))
        while True:
            (packet, client_address) = server_socket.recvfrom(BUFFER)
            self.ParseRequest(packet, client_address, server_socket)


    def ParseRequest(self, packet, client_address, socket):
        action = packet[8:12]
        if action == 0:
            connection_id = random.randrange(10000000, 99999999)
            socket.sendto(0000 + packet[0:8] + connection_id, client_address)
            self.downloaders[str(client_address)] = (str(time.time()) + "#" + str(connection_id) + "#None")
        elif action == 1:
            connection_id = packet[:8]
            currect_time = time.time()
            connection_info = self.downloaders[str(client_address)].split("#")
            if currect_time - int(connection_info[0]) < self.interval:
                if connection_info[1] == connection_id:
                    transaction_id = packet[12:16]








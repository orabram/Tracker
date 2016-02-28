__author__ = 'Or'
import struct
import socket
import time
import random
from SeedersManager import *

BUFFER = 4096
MIN_CONNECTION_ID = 10000000
MAX_CONNECTION_ID = 99999999

class ClientManager():
    def __init__(self, ip, port, seeder_manager):
        self.interval = 120
        self.files = {}
        self.downloaders = {}
        self.ip = ip
        self.port = port
        self.seeder_manager = seeder_manager()

    def wait_for_connections(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((self.ip, self.port))
        while True:
            (packet, client_address) = server_socket.recvfrom(BUFFER)
            self.ParseRequest(packet, client_address, server_socket)

    def ParseRequest(self, packet, client_address, socket):
        packet = struct.unpack(">qii")[0]
        action = int(packet[8:12])
        if action == 0:
            connection_id = random.randrange(MIN_CONNECTION_ID, MAX_CONNECTION_ID)
            transaction_id = packet[12:16]
            packet = action + transaction_id + connection_id
            packet = struct.pack(packet, ">iiq")
            socket.sendto(packet, client_address)
            self.downloaders[str(client_address)] = (str(time.time()) + "#" + str(connection_id) + "#None#None#L")
        elif action == 1:
            packet = struct.unpack(">qiissqqqiiiih")[0]
            connection_id = packet[:8]
            current_time = time.time()
            connection_info = self.downloaders[str(client_address)].split("#")
            if current_time - int(connection_info[0]) < self.interval:
                if connection_info[1] == connection_id:
                    transaction_id = packet[12:16]
                    leechers = len(self.seeder_manager.get_seeders_list())
                    seeders = 0
                    for seeder in self.downloaders:
                        if seeder[len(seeder) - 1] == "L":
                            leechers += 1
                        else:
                            seeders += 1
                    port = packet[96:98]













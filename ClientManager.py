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
            packet = str(action) + transaction_id + connection_id
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
                    event = int(packet[80:84])
                    if event == 1:
                        self.downloaders[str(client_address)][-1] = "S"
                    seeders = len(self.seeder_manager.get_seeders_list()) #seeders = those who've done downloading
                    leechers = 0 #leechers = downloaders
                    for seeder in self.downloaders:
                        if self.downloaders[seeder][-1] == "L":
                            leechers += 1
                        else:
                            seeders += 1
                    port = packet[96:98]
                    if packet[84:88] == 0:
                        ip = client_address
                    else:
                        ip = packet[84:88]
                    interval = self.interval
                    response_packet = str(action) + str(transaction_id) + str(interval) + str(leechers) + str(seeders)
                    max_peers = int(packet[92:96])
                    if max_peers == -1:
                        max_peers = 50
                    counter = 0
                    encode = ""
                    for peer in self.seeder_manager.get_seeders_list():
                        if counter < max_peers:
                            response_packet += str(peer.get_ip)
                            response_packet += str(peer.get_port)
                            encode += "ih"
                            counter += 1
                    if counter < max_peers:
                        for downloader in self.downloaders













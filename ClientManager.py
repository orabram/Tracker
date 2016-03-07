__author__ = 'Or'
import struct
import socket
import time
import random
from SeedersManager import *

BUFFER = 4096
MIN_CONNECTION_ID = 10000000
MAX_CONNECTION_ID = 99999999
CONNECTION_ID_EXPIRED = "The connection id has expired. Please resend an a connect request."
WRONG_CONNECTION_ID = "The connection ID you were attempting to use is incorrect. Please resend a connect request."
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

    def valid_time(self, connection_info):
        current_time = time.time()
        if current_time - int(connection_info[0]) < self.interval:
            return True
        return False

    def valid_connection_id(self, connection_info, connection_id):
        if connection_info[1] == connection_id:
            return True
        return False

    def error_packet(self, message, transaction_id, ip, port, socket):
        action = "0003"
        packet = action + transaction_id + message
        packet = struct.pack(packet, "iis")
        socket.sendto(packet, (ip, port))

    def update_seeder(self, info_hash, connection_info, event, client_address):
        connection_info[-1] == info_hash + "#"
        connection_info[0] == str(time.time()) + "#"
        status = "L"
        if event == 1:
            status = "S"
        self.downloaders[str(client_address)][-1] = "S"

    

    def ParseRequest(self, packet, client_address, socket):
        edited_packet = struct.unpack(">qii", packet)[0]
        action = int(packet[8:12])
        if action == 0:
            connection_id = random.randrange(MIN_CONNECTION_ID, MAX_CONNECTION_ID)
            transaction_id = packet[12:16]
            packet = str(action) + transaction_id + connection_id
            packet = struct.pack(packet, ">iiq")
            socket.sendto(packet, client_address)
            self.downloaders[str(client_address)] = (str(time.time()) + "#" + str(connection_id) + "##L")
        elif action == 1:
            packet = struct.unpack(">qiissqqqiiiih", packet)[0]
            connection_id = packet[:8]
            transaction_id = packet[12:16]
            connection_info = self.downloaders[str(client_address)].split("#")
            if not self.valid_time(connection_info):
                self.error_packet(CONNECTION_ID_EXPIRED, transaction_id, client_address, socket)
            if not self.valid_connection_id(connection_info, connection_id):
                self.error_packet(WRONG_CONNECTION_ID, transaction_id, client_address, socket)
            info_hash = packet[18:36]
            event = int(packet[80:84])
            self.update_seeder(info_hash, connection_info, event, client_address)
            seeders = len(self.seeder_manager.get_seeders_list()) #seeders = those who've done downloading
            leechers = 0 #leechers = downloaders
            for seeder in self.downloaders:
                if self.downloaders[seeder][-1] == "L":
                    leechers += 1
                else:
                    seeders += 1
            port = packet[96:98]
            if packet[84:88] == 0: #If the sent ip is zero, I'll send it back to the sender.
                ip = client_address
            else:
                ip = packet[84:88] #Otherwise, I'll send it to the given ip.
            interval = self.interval
            response_packet = str(action) + str(transaction_id) + str(interval) + str(leechers) + str(seeders)
            max_peers = int(packet[92:96])
            if max_peers == -1:
                max_peers = 50
            counter = 0
            encode = ""
            for peer in self.seeder_manager.get_seeders_list():
                if counter < max_peers:
                    if peer.get_info_hash_list().contains(info_hash):
                        response_packet += str(peer.get_ip)
                        response_packet += str(peer.get_port)
                        encode += "ih"
                        counter += 1
            for downloader in self.downloaders:
                if counter < max_peers:
                    info = downloader.split("#")
                    if info.contains(info_hash):
                        response_packet += str(downloader.get_ip)
                        response_packet += str(downloader.get_port)
                        encode += "ih"
                        counter += 1
                else:
                    break
            response_packet = struct.pack(response_packet, "iiii" + encode)
            socket.sendto(response_packet, (ip, port))
        elif action == 2:
            transaction_id = packet[12:16]
            self.error_packet("The tracker doesn't support scraping at the moment.", transaction_id, client_address, socket)


















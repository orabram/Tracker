#region -------------Info------------
# Name: ClientManager
# Version: 1.0
# By: Or Abramovich
#endregion -------------Info------------

#region -------------Imports---------
import struct
import socket
import time
import random
import os
from SeedersManager import *

#endregion -------------Imports---------

#region -------------Constants--------------
BUFFER = 4096
MIN_CONNECTION_ID = 10000000
MAX_CONNECTION_ID = 99999999
NO_SCRAPE_SUPPORT = "The tracker doesn't support scraping at the moment."
CONNECTION_ID_EXPIRED = "The connection id has expired. Please resend an a connect request."
WRONG_CONNECTION_ID = "The connection ID you were attempting to use is incorrect. Please resend a connect request."
GENERIC_ERROR_MESSEAGE = "An error has occurred. Please attempt to connect to the tracker again."

#endregion -------------Constants--------------

#region -------------Methods&Classes-----------


class ClientManager():
    def __init__(self, ip, port, seeder_manager):
        self.interval = 120
        self.files = {}
        self.downloaders = {}
        self.ip = ip
        self.port = port
        self.seeder_manager = seeder_manager

    def ip2int(self, addr):#Converts ip address to a number.
        return struct.unpack("!I", socket.inet_aton(addr))[0]

    def int2ip(self, addr):#Converts a number into an ip address.
        return socket.inet_ntoa(struct.pack("!I", addr))

    def wait_for_connections(self):#Accepts connections from leechers.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((self.ip, self.port))
        while True:
            (packet, client_address) = server_socket.recvfrom(BUFFER)
            print "connected"
            self.ParseRequest(packet, client_address, server_socket)

    def valid_time(self, connection_info):#Checks if the connection id isn't expired
        current_time = time.time()
        if current_time - int(connection_info[0]) < self.interval:
            return True
        return False

    def valid_connection_id(self, connection_info, connection_id): #Checks if the connection id is valid
        if connection_info[1] == connection_id:
            return True
        return False

    def error_packet(self, message, transaction_id, client_address, socket): #Sends an error packet
        action = 0003
        packet = struct.pack(">ii" + str(len(message)) + "s", action, transaction_id, message)
        socket.sendto(packet,client_address)

    def update_seeder(self, info_hash, connection_info, event, client_address):#Updates the information about the leecher who's downloading the file
        connection_info[-1] = info_hash + "#"
        connection_info[0] = str(time.time()) + "#"
        status = "L"
        if event == 1:
            status = "S"
        self.downloaders[str(client_address)][-1] = "S"

    def sort_seeders_and_leechers(self):
        seeders = len(self.seeder_manager.get_seeders_list()) #seeders = those who've done downloading
        leechers = 0 #leechers = downloaders
        for seeder in self.downloaders:
            if self.downloaders[seeder][-1] == "L":
                leechers += 1
            else:
                seeders += 1
        return seeders, leechers

    def ParseRequest(self, packet, client_address, socket): #Processes a request
        connection_id, action, transaction_id = struct.unpack(">qii", packet[:16])[0]
        if action == 0: #Action == 0 means that this is a connect request
            connection_id = random.randrange(MIN_CONNECTION_ID, MAX_CONNECTION_ID)
            try:
                packet = struct.pack(">iiq", action, transaction_id, connection_id)
                socket.sendto(packet, client_address)
                self.downloaders[str(client_address)] = (str(time.time()) + "#" + str(connection_id) + "##L")
            except:
                self.error_packet(GENERIC_ERROR_MESSEAGE, transaction_id, client_address, socket)
        elif action == 1: #Action == 1 means that this is an announce request.
            connection_id, action, transaction_id, info_hash, peer_id, downloaded, left, uploaded, event, ip, key, num_want, port  = struct.unpack(">qii20s20sqqqiiiih", packet)[0]
            try:
                connection_info = self.downloaders[str(client_address)].split("#")
                if not self.valid_time(connection_info):
                    self.error_packet(CONNECTION_ID_EXPIRED, transaction_id, client_address, socket)
                if not self.valid_connection_id(connection_info, connection_id):
                    self.error_packet(WRONG_CONNECTION_ID, transaction_id, client_address, socket)
                self.update_seeder(info_hash, connection_info, event, client_address)
                seeders, leechers = self.sort_seeders_and_leechers()
                if ip == 0: #If the sent ip is zero, I'll send it back to the sender.
                    ip = client_address
                if num_want == -1:
                    num_want = 50
                counter = 0
                response_packet = struct.pack(">iiiii", action, transaction_id, self.interval, leechers, seeders)
                for peer in self.seeder_manager.get_seeders_list():
                    if counter < num_want:
                        if peer.get_info_hash_list().contains(info_hash):
                            response_packet += struct.pack(">i", self.ip2int(peer.get_ip()))
                            response_packet += struct.pack(">h", peer.get_port())
                            counter += 1
                for downloader in self.downloaders:
                    if counter < num_want:
                        info = downloader.split("#")
                        if info.contains(info_hash):
                            response_packet += struct.pack(">i", self.ip2int(downloader.get_ip()))
                            response_packet += struct.pack(">h", downloader.get_port)
                    else:
                        break
                socket.sendto(response_packet, (ip, port))
            except:
                self.error_packet(GENERIC_ERROR_MESSEAGE, transaction_id, client_address, socket)
        elif action == 2: # Action == 2 is for scraping, which I don't support right now.
            self.error_packet(NO_SCRAPE_SUPPORT, transaction_id, client_address, socket)
        else:
            self.error_packet(GENERIC_ERROR_MESSEAGE, transaction_id, client_address, socket)

    def wait_for_connection(self):
        s = socket.socket()
        s.bind(("0.0.0.0", 9876))
        s.listen(1)
        (client_socket, client_address) = s.accept()
        filename = client_socket.recv(BUFFER)
        for root, dirs, files in os.walk("C:\\"):
            for file in files:
                if file == filename:
                    f = open(os.path.join(root, file), "rb")
                    data = f.read()
                    client_socket.send(data)
                    client_socket.send("done")
                    client_socket.close()
                    break

#endregion -------------Methods&Classes-----------

















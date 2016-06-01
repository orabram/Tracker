#region -------------Info------------
# Name: Tracker Communication Manager
# Version: 1.0
# By: Or Abramovich
#endregion -------------Info------------

#region -------------Imports---------
import socket
import psutil
import os
import math
import Crypto
from Crypto.Hash import SHA
from Crypto import Random
from Crypto.PublicKey import RSA
import time
import pickle
import shutil
import base64
import ast

#endregion -------------Imports---------

#region -------------Constants--------------

SELF_IP = "127.0.0.1"
ENCRYPTION_NUMBER = 32
FILES_LOCATION = "C:\\"
SETTINGS_LOCATION = FILES_LOCATION + "\\" + "settings"
PEER_ID = "-OC000266666666666666-"
CHUNK_SIZE = 128

#endregion -------------Constants--------------

#region -------------Methods&Classes-----------

class TrackerCommunicationManager():
    def __init__(self):
        self.peer_id = PEER_ID # OC stands for Or's Client, 0002 represents the version number(0.2) and the 6's are just random.
        if not os.path.exists(SETTINGS_LOCATION): #Load Information from the settings file.
            os.makedirs(SETTINGS_LOCATION)
        try:
            file = open(SETTINGS_LOCATION + "\\settings.dat", "r")
            self.set_settings(file)
        except: # If he doesn't exist yet, create one using the default values.
            file = open(SETTINGS_LOCATION + "\\settings.dat", "w")
            self.port = 5789
            self.buffer = 16384
            self.files = {}
            file.write()
            file.write("45789")
            file.write("516384")
            pickle.dump(self.files, file)
        file.close()
        self.is_connected = False

    #Reads the settings from the settings.dat file
    def set_settings(self, file):
        file = open(SETTINGS_LOCATION + "\\settings.dat", "r")
        num = int(file.read(1))
        self.port = file.read(num)
        if self.port == "":
            self.port = 5789
        self.port = int(self.port)
        num = int(file.read(1))
        self.buffer = file.read(num)
        if self.buffer == "":
            self.buffer = 16384
        self.buffer = int(self.buffer)
        self.files = pickle.load(file)
        if self.files == "":
            files = {}

    #Connects to the Tracker.
    def connect_to_tracker(self):
        server = socket.socket()
        server.bind((SELF_IP, self.port))
        server.listen(5)
        (self.tracker_socket, tracker_address) = server.accept()
        print "connected"
        self.is_connected = True

    #Calculates the computer's memory, cpu and network usage and sends it to the tracker.
    def get_computer_stats(self):
        cpu_usage = psutil.cpu_percent(interval=0.5) # Gets the CPU usage
        memory = psutil.virtual_memory() # Gets statistics about different memories
        memory_usage = (100 * memory.free / memory.total) # Calculates the percentage of free memory
        network_speed = psutil.net_if_stats() # Gets speeds of different networks
        network_usage = psutil.net_io_counters(pernic=True) # Gets packet usage in different networks in the computer
        counter = 0
        net = ""
        for network in network_usage:
            if network_usage[network].packets_sent > counter: # If a packet was sent through the network, it is the computer's main network.
                counter = network_usage[network].packets_sent
                net = network
        speed = network_speed[net].speed # Get the speed of the network
        self.profile = str(self.calculate_profile(cpu_usage, memory_usage, speed)) # Calculate the profile and update your information
        return self.profile

    def calculate_profile(self, cpu_usage, free_memory, network_activity):
        profile = ((100 - cpu_usage) + free_memory + network_activity) / 3
        return profile

    #Gets a piece of file, returns the hash of that piece.
    def hash_piece(self, piece):
        sha = SHA.new(piece)
        piece = sha.digest()
        return piece

    #Creates the directory's name from the name of the file.
    def get_dir_name(self, filename):
        directory = filename.split(".")
        if len(directory) == 2:
            directory = FILES_LOCATION + directory[0]
        else:
            path = FILES_LOCATION + directory[0]
            for i in xrange(1, len(directory) - 1):
                path += "." + directory[i]
            directory = path
        return directory

    #Updates the settings file.
    def change_files(self, files):
        f = open(SETTINGS_LOCATION + "\\settings.dat", "w")
        f.write(str(len(str(self.port))))
        f.write(str(self.port))
        f.write(str(len(str(self.buffer))))
        f.write(str(self.buffer))
        pickle.dump(files, f)
        f.close()

    #Downloads a piece of the file.
    def download_piece(self, filename, piece_num, size, info_hash):
        piece_num = int(piece_num)
        size = int(size)
        directory = self.get_dir_name(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
            f = open(directory + "\\" + filename, "wb+")
        else:
            try:
                f = open(directory + "\\" + filename, "rb+")
            except:
                f = open(directory + "\\" + filename, "wb+") # Opens the file and creates a new directory if needed.
        confirmation = ""
        while confirmation != "ok":
            self.tracker_socket.send("ready")
            piece = ""
            data = ""
            while data != "done":
                piece += data
                data = self.tracker_socket.recv(self.buffer) # Downloads the piece.
                if data == "": # If the connection has been broken, try to reconnect.
                    self.connect_to_tracker()
                    return
            print "received piece number " + str(piece_num)
            piece_hash2 = self.tracker_socket.recv(self.buffer)
            piece_hash = self.hash_piece(piece)
            if piece_hash == piece_hash2: # Compare piece hashes to make sure that the transfer was successfull.
                confirmation = "ok"
            else:
                confirmation = "notok"
                time.sleep(0.1)
            self.tracker_socket.send(confirmation)
        file_offset = size * (piece_num - 1)
        f.seek(file_offset)
        f.write(piece) # Write to the file the new piece.
        f.close()
        if filename in self.files: # If the file isn't new, add the piece to his list.
            info = self.files[filename]
            info.append(len(piece))
            info.append((piece_num))
            self.files[filename] = info
            self.change_files(self.files)
        else: # If it's new, create a new list for him.
            self.files[filename] = ["safe", info_hash, len(piece), piece_num]
            self.change_files(self.files)

    #Removes the file and its directory.
    def remove_file(self, filename):
        directory = self.get_dir_name(filename)
        os.remove(directory + "\\" + filename)
        shutil.rmtree(directory)
        del self.files[filename]
        self.change_files(self.files)

    def mark_file(self, filename):
        self.tracker_socket.send("ready")
        string_pubkey = self.tracker_socket.recv(self.buffer)
        pubkey = pickle.loads(string_pubkey)
        split_name = filename.split(".")
        split_name.remove(split_name[-1])
        dir_name = FILES_LOCATION + split_name[0]
        for i in split_name[1:]:
            dir_name += "." + i
        f = open(dir_name + "\\" + filename, 'rb')
        content = f.read()
        f.close()
        content = base64.b64encode(content)
        f = open(dir_name + "\\" + filename, 'wb')
        print content
        print type(content)
        encrypted = []
        counter = 0
        for i in xrange(int(math.ceil(len(content) / CHUNK_SIZE)) - 1):
            encrypted.append(pubkey.encrypt(content[int(CHUNK_SIZE) * i: int(CHUNK_SIZE) * (i + 1)], 32))
            counter += 1
        encrypted.append(pubkey.encrypt(content[int(CHUNK_SIZE) * counter:], 32))
        pickle.dump(encrypted, f)
        f.close()
        self.tracker_socket.send("encrypted")

    def unmark_file(self, filename):
        self.tracker_socket.send("ready")
        split_name = filename.split(".")
        split_name.remove(split_name[-1])
        dir_name = FILES_LOCATION + split_name[0]
        for i in split_name[1:]:
            dir_name += "." + i
        f = open(dir_name + "\\" + filename, 'rb')
        encoded_content = pickle.load(f)
        f.close()
        string_encoded_content = pickle.dumps(encoded_content)
        encoded_content2 = pickle.loads(string_encoded_content)
        self.tracker_socket.send(string_encoded_content)
        self.tracker_socket.send("done")
        decrypted_content = ""
        data = self.tracker_socket.recv(self.buffer)
        while data != "done":
            decrypted_content += data
            data = self.tracker_socket.recv(self.buffer)
        print decrypted_content
        content = base64.b64decode(decrypted_content)
        print content
        f = open(dir_name + "\\" + filename, 'wb')
        f.write(content)
        self.tracker_socket.send("decrypted")

    #Processes packets and sends them to where they belong.
    def parse_packet(self):
        packet = self.tracker_socket.recv(self.buffer)
        packet = packet.split("#")
        if packet[0] == "profile":
            self.tracker_socket.send(self.get_computer_stats())
        elif packet[0] == "add":
            filename = packet[1]
            piece_num = packet[2]
            piece_size = packet[3]
            info_hash = packet[4]
            self.download_piece(filename, piece_num, piece_size, info_hash)
        elif packet[0] == "remove":
            self.remove_file(packet[1])
        elif packet[0] == "mark":
            self.mark_file(packet[1])
        elif packet[0] == "unmark":
            self.unmark_file(packet[1])
        elif packet == "":
            self.tracker_socket.close()

    #Return the info_hash of a file.
    def get_info_hash(self, filename):
        for file in self.files:
            if file == filename:
                return self.files[file][2]

    #Return whether or not a file is encrypted.
    def is_file_safe(self, filename):
        for file in self.files:
            if file == filename:
                return self.files[file][0]

    #Return whether or not the seeder is connected to the tracker.
    def is_connected(self):
        return self.is_connected

    #Returns the files that the seeder currently has.
    def get_files(self):
        return self.files

#endregion -------------Methods&Classes-----------







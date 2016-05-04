#region -------------Info------------
# Name: Seeder's Manager
# Version: 1.0
# By: Or Abramovich
#endregion -------------Info------------

#region -------------Imports---------
from Seeder import *
from multiprocessing import Process
#from Tracker import *
import os
import MemoryHandler
import bencode
from Crypto.Hash import SHA
import math
import struct

#endregion -------------Imports---------

#region -------------Constants--------------

TRACKER_PORT = 3456
PIECE_LENGTH = 262144

#endregion -------------Constants--------------

#region -------------Methods&Classes-----------

class seeder_communication_manager():
    def __init__(self):
        self.seeders_list = []

    """def profile_builder(self, stats):
        stats = stats.split(";")
        cpu_usage = stats[1]
        free_memory = stats[2]
        network_activity = stats[3]
        profile = ((100 - cpu_usage) + free_memory + network_activity) / 3
        return profile"""

    #Prints the profile of every seeder.
    def get_seeders_status(self):
        for s in self.seeders_list:
            profile = s.get_computer_stats()

    #Adds a new seeder.
    def add_new_seeder(self, ip, port):
        s = socket.socket()
        s.connect((ip, port))
        seeder = Seeder(ip, port, s)
        self.seeders_list.append(seeder)
        return "A seeder was successfully added."

    #Removes a seeder.
    def remove_seeder(self, ip):
        for s in self.seeders_list:
            if s.get_ip() == ip:
                s.get_socket().close()
                self.seeders_list.remove(s)
                return "The seeder has been removed."
            else:
                return "The seeder does not exist. Please make sure that you've entered the correct IP address and try again."

    #This one is for easy transfer through sockets.
    def get_seeders_list(self):
        seeders_list = ""
        for i in self.seeders_list:
            seeders_list += "#" + str(i.get_ip())
        return seeders_list

    #This one is for the actual list.
    def get_seeders_list2(self):
        return self.seeders_list

    def set_seeders_list(self, list):
        self.seeders_list = list

    #Creates a 20 bytes SHA1 sequence from a piece of information.
    def hash_piece(self, piece):
        sha = SHA.new(piece)
        piece = sha.digest()
        return piece

    # Divides the file between all the seeders.
    def divide_files(self, path):
        try:
            file = open(path, "rb")
        except:
            return "The path you've entered is incorrect."
        filename = path.split("\\")[-1]
        counter = 0
        seeders = []
        pieces = []
        pieces_hash = ""
        data = ""
        for s in self.seeders_list:
            #if s.get_profile() > 30:
            seeders.append(s)
        file_length = os.stat(path).st_size
        print file_length
        file_length = int(os.stat(path).st_size)
        print file_length
        """try:
            piece_length = int(math.ceil(file_length / counter))
        except:
            return "There are no optional seeders right now."
        true_counter = counter + 1
        if piece_length > MAX_PIECE_LENGTH:
            while int(math.ceil(file_length / counter)) > MAX_PIECE_LENGTH:
                true_counter += 1"""
        while True:
            filedata = file.read(PIECE_LENGTH)
            if len(filedata) == 0:
                break
            data += filedata
            if len(data) >= PIECE_LENGTH:
                pieces_hash += self.hash_piece(data[:PIECE_LENGTH])
                pieces.append(data)
                data = data[PIECE_LENGTH:]#Reads the piece, stores the piece and its hash.
                counter += 1
        if len(data) > 0:
            pieces_hash += self.hash_piece(data)
            pieces.append(data)
            counter += 1
        info_hash = self.build_meta_file(path, file_length, PIECE_LENGTH, pieces_hash) #Creates a metadata file
        j = 0
        print "got here"
        message = ""
        for i in xrange(counter):# Spreads the file between the seeders.
            try:
                message = seeders[j].add_new_file(filename, pieces[i], info_hash, i + 1, PIECE_LENGTH, pieces_hash[i*20:i*20 + 20])
                j += 1
            except:
                j = 0
                i -= 1
            if message == "disconnected":
                self.remove_seeder(seeders[j].get_ip())
        return "The file has been added."

    #Builds a metadata file.
    def build_meta_file(self, path, file_length, piece_length, pieces_hash):
        port = TRACKER_PORT.__str__()
        ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1][0] #Gets the IP and port of the tracker.
        announce = "udp://" + ip + ":" + port + "/announce" #Creates an announce URL.
        filename = path.split("\\")[-1]
        temp = filename.split(".")
        temp[-1] = "torrent"
        torrent_name = temp[0]
        for i in temp[1:]:
            torrent_name += "." + i #turns the file into a .torrent file
        info = {'name' : filename, 'piece length': piece_length, 'length': file_length, 'pieces': pieces_hash }
        file = {"announce" : announce, "info" : info} #Builds the info dictionary and the file
        print file
        MemoryHandler.save_file(torrent_name, bencode.bencode(file)) #Saves them as bencoded data
        return self.hash_piece(bencode.bencode(info)) #Returns the info_hash

    #Removes a file.
    def remove_files(self, path):
        filename = path.split("\\")[-1]
    #try:
        for s in self.seeders_list:
            if filename in s.get_files_list():
                s.remove_file(filename)
                print s.get_files_list()
        return "The file has been successfully removed."
    #except:
        #return "A problem has occurred."

    def mark_as_suspicious(self, filename):
        for s in self.seeders_list:
            if s.get_files_list().contains(filename):
                s.mark_as_suspicious(filename)

    def mark_as_safe(self, filename):
        for s in self.seeders_list:
            if s.get_files_list().contains(filename):
                s.mark_as_safe(filename)

#endregion -------------Methods&Classes-----------









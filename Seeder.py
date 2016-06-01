#region -------------Info------------
# Name: Seeder
# Version: 1.0
# By: Or Abramovich
#endregion -------------Info------------

#region -------------Imports---------
import socket
import os
import time
import math
import pickle

#endregion -------------Imports---------

#region -------------Constants--------------

BUFFER = 4096
CHUNK_SIZE = 128
#endregion -------------Constants--------------

#region -------------Methods&Classes-----------

class Seeder():
    def __init__(self, ip, port, socket):
        self.ip = ip
        self.port = port
        self.socket = socket
        self.files = {}
        self.files_list = []
        self.info_hash_list = []
        self.profile = 0

    # Encrypts a file
    def mark_suspicious_files(self, filename, encryptor, path):
        self.socket.send("mark#" + filename)
        confirmation = self.socket.recv(BUFFER)
        if confirmation == "":
            exit(0)
        if confirmation == "ready":
            key = encryptor.generate_keys()
            pubkey = encryptor.get_pub_key(key)
            string_key = pickle.dumps(pubkey)
            self.socket.send(string_key)
            key2 = pickle.dumps(key)
            self.socket.send(key2)
            confirmation = self.socket.recv(BUFFER)
            if confirmation == "":
                return "disconnected"
            elif confirmation == "encrypted":
                encryptor.create_key_pair(filename, key)
        self.files[filename][0] = "suspicious"
        return "The file has been encrypted successfully"

    # Decrypts a file
    def mark_as_safe(self, filename, encryptor, path):
        self.socket.send("unmark#" + filename)
        confirmation = self.socket.recv(BUFFER)
        encrypted_data = ""
        if confirmation == "":
            return "disconnected"
        if confirmation == "ready":
            data = self.socket.recv(BUFFER)
            while data != "done":
                encrypted_data += data
                data = self.socket.recv(BUFFER)
            encrypted = pickle.loads(encrypted_data)
            key = encryptor.get_key(filename)
            decrypted = ""
            for i in xrange(len(encrypted)):
                decrypted += encryptor.decrypt_message(key, encrypted[i])
            self.socket.send(decrypted)
            self.socket.send("done")
            confirmation = self.socket.recv(BUFFER)
        if confirmation == "decrypted":
            self.files[filename][0] = "safe"
            return "The file has been decrypted successfully"
        else:
            return "a bug has occurred"

    # Removes a file
    def remove_file(self, filename):
        self.socket.send("remove#" + filename)
        info_hash = self.files[filename][1]
        self.files.pop(filename)
        self.files_list.remove(filename)
        self.info_hash_list.remove(info_hash)
        return "removed"

    # Adds a file
    def add_new_file(self, filename, chunk, info_hash, piece_num, piece_length, piece_hash):
        confirm = ""
        print "got here 2"
        self.socket.send("add#" + filename + "#" + str(piece_num) + "#" + str(piece_length) + "#" + info_hash)
        while confirm != "ok":
            confirmation = self.socket.recv(BUFFER)
            if confirmation == "ready":
                self.socket.send(chunk)
            print "sent piece number" + str(piece_num)
            time.sleep(0.01)
            self.socket.send("done")
            self.socket.send(piece_hash)
            confirm = self.socket.recv(BUFFER)
            if confirm == "":
                print "The client has disconnected"
                return "disconnect"
        if self.files_list.__contains__(filename):
            pieces = self.files_list[filename]
            self.files[filename] = pieces.append(piece_num)
        else:
            self.files_list.append(filename)
            self.info_hash_list.append(info_hash)
            self.files[filename] = ["safe", info_hash]
        return "completed"

    # Returns the machine's profile
    def get_computer_stats(self):
        self.socket.send("profile")
        self.profile = float(self.socket.recv(BUFFER))
        return self.profile

    def set_profile(self, profile):
        self.profile = profile

    def get_profile(self):
        return self.profile

    def get_ip(self):
        return self.ip

    def get_files(self):
        return self.files

    def get_files_list(self):
        return self.files_list

    def get_info_hash_list(self):
        return self.info_hash_list

    def get_port(self):
        return self.port

    def get_socket(self):
        return self.socket

#endregion -------------Methods&Classes-----------
#region -------------Info------------
# Name: Seeder
# Version: 1.0
# By: Or Abramovich
#endregion -------------Info------------

#region -------------Imports---------
import socket
import os
import time

#endregion -------------Imports---------

#region -------------Constants--------------

BUFFER = 4096

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

    def mark_suspicious_files(self, filename):
        self.socket.send("mark#" + filename)
        info_hash = self.files[filename][1]
        self.files[filename] = ["suspicious", info_hash]

    def mark_as_safe(self, filename):
        self.socket.send("unmark#" + filename)
        info_hash = self.files[filename][1]
        self.files[filename] = ["safe", info_hash]

    def remove_file(self, filename):
        self.socket.send("remove#" + filename)
        info_hash = self.files[filename][1]
        self.files.pop(filename)
        self.files_list.remove(filename)
        self.info_hash_list.remove(info_hash)
        return "removed"

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
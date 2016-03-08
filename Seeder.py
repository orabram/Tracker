__author__ = 'Or'
import socket
import os

BUFFER = 4096

class Seeder():
    def __int__(self, ip, port, socket):
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
        #os.remove(os.path.abspath(filename))
        self.files_list.remove(filename)
        self.info_hash_list.remove(info_hash)

    def add_new_file(self, filename, chunks, info_hash):
        self.socket.send("add#" + filename)
        self.socket.send(chunks)
        self.files[filename] = ["safe", info_hash]
        self.files_list.append(filename)
        self.info_hash_list.append(info_hash)

    def modify_files_list(self, files):
        self.socket.send("files#" + files)

    def get_computer_stats(self):
        self.socket.send("profile")
        return self.socket.recv(BUFFER)

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

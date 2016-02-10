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
        self.profile = 0

    def mark_suspicious_files(self, filename):
        self.socket.send("mark#" + filename)
        self.files[filename] = "suspicious"

    def mark_as_not_suspicious(self, filename):
        self.socket.send("unmark#" + filename)
        self.files[filename] = "safe"

    def remove_file(self, filename):
        self.socket.send("remove#" + filename)
        self.files.pop(filename)
        os.remove(os.path.abspath(filename))
        self.files_list.remove(filename)

    def add_new_file(self, filename, chunks):
        self.socket.send("add#" + filename)
        self.socket.send(chunks)
        self.files[filename] = "safe"
        self.files_list.append(filename)

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

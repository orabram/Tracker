__author__ = 'Or'
import socket

BUFFER = 4098

class Seeder():
    def __int__(self, ip, port, socket):
        self.ip = ip
        self.port = port
        self.socket = socket
        self.files = {}
        self.profile = 0

    def mark_suspicious_files(self, filename):
        self.socket.send("mark#" + filename)
        self.files[filename] = "suspicious"

    def mark_as_not_suspicious(self, filename):
        self.socket.send("unmark#" + filename)
        self.files[filename] = "safe"

    def remove_file(self, filename):
        self.socket.send("remove#" + filename)
        self.files.remove(filename)

    def add_new_file(self, filename, chunks):
        self.socket.send("add#" + filename)
        self.socket.send(chunks)
        self.files[filename] = "safe"

    def modify_files_list(self, new_list):
        self.socket.send("list#" + new_list)
        self.files = new_list

    def get_computer_stats(self):
        self.socket.send("profile")
        return self.socket.recv(BUFFER)

    def set_profile(self, profile):
        self.profile = profile

    def get_profile(self):
        return self.profile
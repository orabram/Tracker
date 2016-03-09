__author__ = 'Or'

import socket
from SeedersManager import *

IP = "127.0.0.1"
PORT = 6666
GUI_PORT = 6666
BUFFER = 4096

class gui_manager():
    def __init__(self, seeders_manager):
        self.port = PORT
        self.ip = IP
        self.manager = seeders_manager
        self.gui = ""

    def establish_connection(self):
        gui = socket.socket()
        gui.bind((IP, GUI_PORT))
        gui.connect((self.ip, self.port))
        self.gui = gui

    def send_computers_list(self):
        self.gui.send(self.manager.get_seeders_list())

    def get_new_commands(self):
        command = self.gui.recv(BUFFER)
        command = command.split(" ")
        if command[0] == "adds":
            self.manager.add_new_seeder(command[1], command[2])
        elif command[0] == "removes":
            self.manager.remove_seeder(command[1])
        elif command[0] == "addf":
            self.manager.divide_files(command[1], command[2])
        elif command[0] == "removef":
            self.manager.remove_files(command[1])
        elif command[0] == "mark":
            self.manager.mark_as_suspicious(command[1])
        elif command[0] == "unmark":
            self.manager.mark_as_safe(command[1])



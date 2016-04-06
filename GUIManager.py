__author__ = 'Or'

import socket
from SeedersManager import *

IP = "127.0.0.1"
PORT = 5555
GUI_PORT = 6666
BUFFER = 4096

class gui_manager():
    def __init__(self, seeders_manager):
        self.manager = seeders_manager

    def establish_connection(self):
        gui = socket.socket()
        gui.bind((IP, PORT))
        gui.connect((IP, GUI_PORT))
        self.gui = gui

    def send_computers_list(self):
        self.gui.send(self.manager.get_seeders_list())

    def get_new_commands(self):
        command = self.gui.recv(BUFFER)
        command = command.split("#")
        if command[0] == "adds":
            self.manager.add_new_seeder(command[1], command[2])
        elif command[0] == "removes":
            error_message = self.manager.remove_seeder(command[1])
            self.gui.send("rs#" + error_message)
        elif command[0] == "addf":
            error_message = self.manager.divide_files(command[1])
            self.gui.send("af#" + error_message)
        elif command[0] == "removef":
            self.manager.remove_files(command[1])
        elif command[0] == "mark":
            self.manager.mark_as_suspicious(command[1])
        elif command[0] == "unmark":
            self.manager.mark_as_safe(command[1])



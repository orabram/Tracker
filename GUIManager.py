__author__ = 'Or'
#region -------------Info------------
# Name: GUIManager
# Version: 1.0
# By: Or Abramovich
#endregion -------------Info------------

#region -------------Imports---------
import socket
from SeedersManager import *


#endregion -------------Imports---------

#region -------------Constants--------------

IP = "127.0.0.1"
PORT = 5555
GUI_PORT = 6666
BUFFER = 4096

#endregion -------------Constants--------------

#region -------------Methods&Classes-----------

class gui_manager():
    def __init__(self, seeders_manager):
        self.manager = seeders_manager

    def establish_connection(self):
        gui = socket.socket()
        gui.bind((IP, PORT))
        gui.connect((IP, GUI_PORT))
        self.gui = gui

    def send_computers_list(self):
        self.gui.send("list" + self.manager.get_seeders_list())
        return "The list has been refreshed."

    def get_new_commands(self):
        command = self.gui.recv(BUFFER)
        command = command.split("#")
        if command[0] == "adds":
            print "adding seeder request"
            error_message = self.manager.add_new_seeder(command[1], int(command[2]))
            self.gui.send(error_message)
            print "request fulfilled"
        elif command[0] == "removes":
            print "remove seeder request"
            error_message = self.manager.remove_seeder(command[1])
            self.gui.send(error_message)
            print "request fulfilled"
        elif command[0] == "addf":
            print "adding file request"
            error_message = self.manager.divide_files(command[1])
            self.gui.send(error_message)
            print "request fulfilled"
        elif command[0] == "removef":
            print "remove file request"
            error_message = self.manager.remove_files(command[1])
            self.gui.send(error_message)
            print "request fulfilled"
        elif command[0] == "mark":
            self.manager.mark_as_suspicious(command[1])
        elif command[0] == "unmark":
            self.manager.mark_as_safe(command[1])
        elif command[0] == "info":
            print "information request"
            for s in self.manager.get_seeders_list2():
                if s.get_ip() == command[1]:
                    if s.get_profile() == 0:
                        profile = s.get_computer_stats()
                    message = "IP:" + s.get_ip() + "\r\nPort = " + str(s.get_port()) + "\r\nProfile = " + str(s.get_profile()) + "\r\nFiles = " + str(s.get_files_list())
                    self.gui.send("info#" + message)
            print "request fulfilled"
        elif command[0] == "refresh":
            print "refresh request"
            error_message = self.send_computers_list()
            self.gui.send(error_message)
            print "request fulfilled"

#endregion -------------Methods&Classes-----------



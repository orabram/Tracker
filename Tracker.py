__author__ = 'Or'
from ClientManager import *
from SeedersManager import *
from GUIManager import *
import socket
import struct
from multiprocessing import Process

SELF_IP = "0.0.0.0"
GUI_PORT = 6666
TRACKER_PORT = 3456

def start_processes():
    p = Process(target=clients_manager.wait_for_connections)
    p.start()
    p = Process(target=connect_to_gui, args=[gui_manager])
    p.start()
    p = Process(target=get_new_commands)


def connect_to_gui(gui_manager):
    gui_manager.establish_connection()
    time1 = time.time()
    while True:
        if time.time() - time1 > 120:
            time1 = time.time()
            gui_manager.send_computers_list()


def get_new_commands():


seeders_manager = seeder_communication_manager()
clients_manager = ClientManager(SELF_IP, TRACKER_PORT, seeders_manager)
gui_manager = gui_manager()




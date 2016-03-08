__author__ = 'Or'
from ClientManager import *
from SeedersManager import *
from GUIManager import *
import socket
import struct
from multiprocessing import Process

SELF_IP = "0.0.0.0"
TRACKER_PORT = 3456
GUI_INTERVAL = 120
SEEDERS_INTERVAL = 300

def start_processes():
    p = Process(target=clients_manager.wait_for_connections)
    p.start()
    p = Process(target=connect_to_gui, args=[gui_manager])
    p.start()
    p = Process(target=get_new_commands, args=[gui_manager])
    p.start()
    p = Process(target=update_seeders, args=[seeders_manager])
    p.start()

def connect_to_gui(gui_manager):
    gui_manager.establish_connection()
    time1 = time.time()
    while True:
        if time.time() - time1 >= GUI_INTERVAL:
            time1 = time.time()
            gui_manager.send_computers_list()


def get_new_commands(gui_manager):
    while True:
        gui_manager.get_new_commands()

def update_seeders(seeders_manager):
    time1 = time.time()
    while True:
        if time.time() - time >= SEEDERS_INTERVAL:
            seeders_manager.get_seeders_status()



seeders_manager = seeder_communication_manager()
clients_manager = ClientManager(SELF_IP, TRACKER_PORT, seeders_manager)
gui_manager = gui_manager(seeders_manager)
start_processes()






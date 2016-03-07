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

seeders_manager = seeder_communication_manager()
clients_manager = ClientManager(SELF_IP, TRACKER_PORT, seeders_manager)




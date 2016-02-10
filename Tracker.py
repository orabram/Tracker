__author__ = 'Or'
from Seeder import *
from SeedersManager import *
from GUIManager import *
import socket
import struct
from multiprocessing import Process

SELF_IP = "0.0.0.0"
GUI_PORT = 6666




seedersmanager = seeder_communication_manager()



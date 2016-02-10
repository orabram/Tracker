__author__ = 'Or'
from Seeder import *
from SeedersManager import *
from GUIManager import *
import socket
import struct
from multiprocessing import Process

SELF_IP = "0.0.0.0"
SELF_PORTS = [6881, 6882, 6883, 6884, 6885, 6886, 6887, 6888, 6889]




seedersmanager = seeder_communication_manager()



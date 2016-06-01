import bencode
import os
from SeedersManager import *
from ClientManager import *

seeders_manager = seeder_communication_manager()
clients_manager = ClientManager("127.0.0.1", 3456, seeders_manager)

clients_manager.wait_for_connection()
from ClientManager import *
SELF_IP = "127.0.0.1"
TRACKER_PORT = 3456


seeders_manager = seeder_communication_manager()
clients_manager = ClientManager(SELF_IP, TRACKER_PORT, seeders_manager)

clients_manager.wait_for_connections()
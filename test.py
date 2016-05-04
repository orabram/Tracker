from GUIManager import *
from SeedersManager import *
from threading import Thread

SELF_IP = "0.0.0.0"
TRACKER_PORT = 3456
GUI_INTERVAL = 15
SEEDERS_INTERVAL = 600

def start_processes():
    t1 = Thread(target=connect_to_gui, args=[gui_manager])
    t1.start()
    t2 = Thread(target=get_new_commands, args=[gui_manager])
    t2.start()
    t3 = Thread(target=update_seeders, args=[seeders_manager])
    t3.start()
    # t4 = Thread(target=clients_manager.wait_for_connections)
    # t4.start()

def connect_to_gui(gui_manager):
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
        if time.time() - time1 >= float(SEEDERS_INTERVAL):
            seeders_manager.get_seeders_status()

if __name__ == '__main__':
    seeders_manager = seeder_communication_manager()
    gui_manager = gui_manager(seeders_manager)
    gui_manager.establish_connection()
    start_processes()

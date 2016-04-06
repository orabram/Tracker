from GUIManager import *
from SeedersManager import *
manager = seeder_communication_manager()
gui = gui_manager(manager)
gui.establish_connection()
while True:
    gui.get_new_commands()

#region -------------Info------------
# Name: Client
# Version: 1.0
# By: Or Abramovich
#endregion -------------Info------------

#region -------------Imports---------
from TrackerCommunicationManager import *
from ClientCommunication import *
import time
from multiprocessing import Process

#endregion -------------Imports---------

#region -------------Constants--------------

IP = "0.0.0.0"
PORT = 6881

#endregion -------------Constants--------------

#region -------------Methods&Classes-----------

def start_processes(tracker_communicator):
    p = Process(target=connect_to_tracker, args=[tracker_communicator])
    p.start()
    #manage_downloads(tracker_communicator)

def connect_to_tracker(tracker_communicator):
    tracker_communicator.connect_to_tracker()
    while tracker_communicator.is_connected():
        tracker_communicator.parse_information()

def manage_downloads(tracker_communicator):
    s = socket.socket()
    s.bind((IP, PORT))
    s.listen(5)
    while True:
        (peer_socket, peer_address) = s.accept()
        peer_communicator = ClientCommunication(peer_socket, tracker_communicator)
        p = Process(target=ClientCommunication.manage_download)
        p.start()

#endregion -------------Methods&Classes-----------

#region ----------Main--------

if __name__ == '__main__':
    tracker_communicator = TrackerCommunicationManager()
    start_processes(tracker_communicator)

#endregion --------Main---------
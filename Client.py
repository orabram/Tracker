__author__ = 'Or'
from TrackerCommunicationManager import *
from ClientCommunication import *
import time
from multiprocessing import Process

IP = "0.0.0.0"
PORT = 6881


def start_processes(tracker_communicator):
    p = Process(target=connect_to_tracker, args=[tracker_communicator])
    p.start()
    p = Process(target=manage_downloads)
    p.start()

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

tracker_communicator = TrackerCommunicationManager()
start_processes(tracker_communicator)
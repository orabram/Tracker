import socket
from  ClientCommunication import *
from TrackerCommunicationManager import *
from multiprocessing import Process
SELF_IP = "0.0.0.0"
SELF_PORT = 4206


def manage_downloads(tracker_communicator):
    s = socket.socket()
    s.bind((SELF_IP, SELF_PORT))
    s.listen(5)
    while True:
        (peer_socket, peer_address) = s.accept()
        peer_communicator = ClientCommunication(peer_socket, tracker_communicator)
        p = Process(target=ClientCommunication.manage_download)
        p.start()

tracker_communicator = TrackerCommunicationManager()
manage_downloads(tracker_communicator)
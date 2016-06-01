from threading import Thread
import socket
from ClientCommunication import *

IP = "127.0.0.1"
PORT = 6881
def manage_downloads(tracker_communicator):
    s = socket.socket()
    s.bind((IP, PORT))
    s.listen(5)
    while True:
        (peer_socket, peer_address) = s.accept()
        peer_communicator = ClientCommunication(peer_socket, tracker_communicator)
        p = Thread(target=ClientCommunication.manage_download)
        p.start()

tracker_communicator = TrackerCommunicationManager()
manage_downloads(tracker_communicator)


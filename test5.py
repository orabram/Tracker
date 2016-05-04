import bencode
import socket
from TrackerCommunicationManager import *
tracker_communicator = TrackerCommunicationManager()
tracker_communicator.connect_to_tracker()
while True:
    tracker_communicator.parse_packet()

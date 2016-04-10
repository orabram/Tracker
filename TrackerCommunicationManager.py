__author__ = 'Or'
import socket
import psutil
import os
import math

SELF_IP = "0.0.0.0"
SELF_PORT = 4206
BUFFER = 16384
FILES_LOCATION = "will_be_decided_later"

class TrackerCommunicationManager():
    def __init__(self):
        self.peer_id = "-OC000266666666666666-" # OC stands for Or's Client, 0002 represents the version number(0.2) and the 6's are just random.
        self.files = {}
        self.is_connected = False

    def connect_to_tracker(self):
        server = socket.socket()
        server.bind((SELF_IP, SELF_PORT))
        server.listen(1)
        (self.tracker_socket, tracker_address) = server.accept()
        print "connected"
        self.is_connected = True

    def send_computer_stats(self):
        cpu_usage = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        memory_usage = (100 * memory.free / memory.total)
        network_speed = psutil.net_if_stats()
        network_usage = psutil.net_io_counters(pernic=True)
        counter = 0
        net = ""
        for network in network_usage:
            if network_usage[network].packets_sent > counter:
                counter = network_usage[network].packets_sent
                net = network
        speed = network_speed[net].speed
        self.tracker_socket.send(cpu_usage, memory_usage, speed)

    def download_piece(self, filename, piece_num, size, info_hash):
        f = open(filename + ".txt", "rb+")
        self.tracker_socket.send("ready")
        counter = int(math.ceil(size / BUFFER))
        data = ""
        for i in xrange(counter):
            data += self.tracker_socket.recv(BUFFER)
        data += self.tracker_socket.recv(BUFFER)
        file_offset = size * (piece_num - 1)
        f.seek(file_offset)
        f.write(data)
        self.files[filename] = ["safe", piece_num, info_hash, size]

    def remove_piece(self, filename):
        script_dir = os.path.dirname(filename)
        abs_file_path = os.path.join(script_dir, FILES_LOCATION)
        os.remove(abs_file_path)

    def mark_piece(self, filename):
        print 1

    def unmark_piece(self, filename):
        print 2

    def parse_packet(self):
        packet = self.tracker_socket.recv(BUFFER)
        packet = packet.split("#")
        if packet[0] == "profile":
            self.send_computer_stats()
        elif packet[0] == "add":
            filename = packet[1]
            piece_num = packet[2]
            piece_size = packet[3]
            info_hash = packet[4]
            self.download_piece(filename, piece_num, piece_size, info_hash)
        elif packet[0] == "remove":
            self.remove_piece(packet[1])
        elif packet[0] == "mark":
            self.mark_piece(packet[1])
        elif packet[0] == "unmark":
            self.unmark_piece(packet[1])
        elif packet == "":
            self.tracker_socket.close()

    def get_info_hash(self, filename):
        for file in self.files:
            if file == filename:
                return self.files[file][2]

    def get_piece_num(self, filename):
        for file in self.files:
            if file == filename:
                return self.files[file][1]

    def is_file_safe(self, filename):
        for file in self.files:
            if file == filename:
                return self.files[file][0]

    def is_connected(self):
        return self.is_connected

    def get_files(self):
        return self.files









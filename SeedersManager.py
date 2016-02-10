__author__ = 'Or'

from Seeder import *
from multiprocessing import Process


class seeder_communication_manager():
    def __init__(self):
        self.seeders_list = []

    def profile_builer(self, stats):
        stats = stats.split(";")
        cpu_usage = stats[1]
        free_memory = stats[2]
        network_activity = stats[3]
        profile = cpu_usage + free_memory + network_activity
        return profile

    def get_seeders_status(self):
        for s in self.seeders_list:
            s.modify_files_list(s.files)
            s.set_profile(self.profile_builder(s.get_computer_stats()))

    def add_new_seeder(self, ip, port):
        s = socket.socket()
        s.connect((ip, port))
        seeder = Seeder(ip, port, socket)
        self.seeders_list.append(seeder)

    def remove_seeder(self, ip):
        for s in self.seeders_list:
            if s.get_ip() == ip:
                self.seeders_list.remove(s)
                break

    def get_seeders_list(self):
        return self.seeders_list

    def set_seeders_list(self, list):
        self.seeders_list = list

    def divide_files(self, filename):
        f = open(filename, "r")
        file = f.read()
        counter = 0
        counter2 = 0
        for s in self.seeders_list:
            if s.get_profile() < 7:
                counter += 1
        for s in self.seeders_list:
            if s.get_profile() < 7:
                if (len(file) / counter) * (counter2 + 1) < 1:
                    s.add_new_file(file[(len(file) / counter) * counter2:(len(file) / counter) * (counter2 + 1)])
                    counter2 += 1
                else:
                    s.add_new_file(file[(len(file) / counter) * counter2:])
    def remove_files(self, filename):
        for s in self.seeders_list:
            try:
                s.get_files_list.remove(filename)
                s.remove_file(filename)
    








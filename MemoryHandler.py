#region -------------Info------------
# Name: memory handler
# Version:1.1
# By: Or Abramovich
#     Yaniv Sharon
#endregion -------------Info------------

#region -------------Imports---------
import os
import time
import socket
from Crypto.Hash import SHA512
#endregion -------------Imports---------

#region -------------Methods-----------


def get_server_settings():
    settings = {}
    settings_location = os.path.dirname(os.path.abspath(__file__)) + '\\Files\\Private Server Files\\server settings.cfg'
    settings_file = open(settings_location, 'r')
    settings_list = settings_file.read().split('\n')
    for setting in settings_list:
        if setting[0] != '#':
            setting = setting.split('=', 1)
            settings[setting[0]] = setting[1]
    settings_file.close()
    settings['domain'] = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1][0]
    return settings


def get_server_file(file_name):
    file_location = os.path.dirname(os.path.abspath(__file__)) + '\\Files\\Public Server Files\\' + file_name
    if not os.path.isfile(file_location):
        return False, ''
    file = open(file_location, 'rb')
    file_info = file.read()
    file.close()
    return True, file_info


def save_file(file_name, file_data, password=''):
    splitted_file_name = file_name.split('.')
    if len(splitted_file_name) != 1:
        file_ext = splitted_file_name[-1]
        file_name = file_name[: - len(file_ext) - 1]
    else:
        file_ext = ''
    if file_name == 'temp' or file_name == 'storage info' or file_name == '':
        return False
    sha = SHA512.new('')
    if password == sha.hexdigest():
        password = ''
    storage_location = os.path.dirname(os.path.abspath(__file__)) + '\\Files\\Storage'
    inserted_file_info = '%s:%s:%s:%s' % (file_name, file_ext, password, time.strftime('%d/%b/%Y', time.gmtime()))
    info_location = storage_location + '\\storage info.txt'
    info_file = open(info_location, 'r')
    info_file_data = info_file.read()
    info_file.close()
    if info_file_data == '':
        file_list = [inserted_file_info]
        file_saved = True
    else:
        file_list = info_file_data.split('\n')
        file_saved = False
        for file_index, file_info in enumerate(file_list):
            checked_file_name = file_info.split(':')[0]
            if checked_file_name == file_name:
                if get_file(file_name, password)[0]:
                    delete_file(file_name, password)
                    file_list[file_index] = inserted_file_info
                    file_saved = True
                    print 'file saved: ', file_name
                    break
                else:
                    file_saved = False  # The name is taken and therefore the file was not saved.
                    print 'file not saved: ', file_name
                    break
            elif checked_file_name > file_name:
                file_list.insert(file_index, inserted_file_info)
                file_saved = True
                print 'file saved: ', file_name
                break
            elif file_info == file_list[-1]:
                file_list.append(inserted_file_info)
                file_saved = True
                print 'file saved: ', file_name
                break
    if file_saved:
        if file_ext == '':
            new_file = open('%s\\%s' % (storage_location, file_name), 'wb')
        else:
            new_file = open('%s\\%s.%s' % (storage_location, file_name, file_ext), 'wb')
        new_file.write(file_data)
        new_file.close()
        new_info_file = open(storage_location + '\\temp.txt', 'w')
        new_info_file_data = ''
        for file_info in file_list:
            new_info_file_data += file_info + '\n'
        new_info_file.write(new_info_file_data[:-1])
        os.remove(info_location)
        new_info_file_name = new_info_file.name
        new_info_file.close()
        os.renames(new_info_file_name, storage_location + '\\storage info.txt')
    return file_saved



def hash_save_file(file_name, password, file_data):
    sha = SHA512.new(password)
    password = sha.hexdigest()
    return save_file(file_name, password, file_data)


def get_file(file_name, password=''):
    splitted_file_name = file_name.split('.')
    alt_file_name = file_name[: - len(splitted_file_name[-1]) - 1]
    storage_location = os.path.dirname(os.path.abspath(__file__)) + '\\Files\\Storage'
    info_location = storage_location + '\\storage info.txt'
    info_file = open(info_location, 'r')
    file_list = info_file.read().split('\n')
    info_file.close()
    first = 0
    last = len(file_list)-1
    info = None
    while first <= last and info is None:
        midpoint = (first + last)//2
        if file_list[midpoint].split(':')[0] == file_name or file_list[midpoint].split(':')[0] == alt_file_name:
            info = file_list[midpoint].split(':')
        else:
            if file_name < file_list[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1
    if info is None:
        return False, 'File not found'
    if info[2] != password and not info[2] == '':
        return False, 'Incorrect password (get shreked scrub)'
    if info[1] == '':
        return True, open('%s\\%s' % (storage_location, info[0]), 'rb')
    return True, open('%s\\%s.%s' % (storage_location, info[0], info[1]), 'rb')


def hash_get_file(file_name, password):
    sha = SHA512.new(password)
    password = sha.hexdigest()
    return get_file(file_name, password)


def delete_file(file_name, password):
    splitted_file_name = file_name.split('.')
    alt_file_name = file_name[: - len(splitted_file_name[-1]) - 1]
    storage_location = os.path.dirname(os.path.abspath(__file__)) + '\\Files\\Storage'
    info_location = storage_location + '\\storage info.txt'
    info_file = open(info_location, 'r')
    file_list = info_file.read().split('\n')
    info_file.close()
    first = 0
    last = len(file_list)-1
    info = None
    midpoint = None
    while first <= last and info is None:
        midpoint = (first + last)//2
        if file_list[midpoint].split(':')[0] == file_name or file_list[midpoint].split(':')[0] == alt_file_name:
            info = file_list[midpoint].split(':')
        else:
            if file_name < file_list[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1
    if info is None:
        return False, 'File not found'
    if info[2] != password and not info[2] == '':
        return False, 'Incorrect password (get shreked scrub)'
    os.remove('%s\\%s.%s' % (storage_location, info[0], info[1]))
    file_list.remove(file_list[midpoint])
    new_info_file = open(storage_location + '\\temp.txt', 'w')
    new_info_file_text = ''
    for file_info in file_list:
        new_info_file_text += file_info + '\n'
    new_info_file.write(new_info_file_text[:-1])
    os.remove(info_location)
    new_info_file_name = new_info_file.name
    new_info_file.close()
    os.renames(new_info_file_name, storage_location + '\\storage info.txt')
    return True, 'File removed'


def hash_delete_file(file_name, password):
    sha = SHA512.new(password)
    password = sha.hexdigest()
    return delete_file(file_name, password)
#endregion -------------Methods-----------
# region -------------Info------------
# Name: request handler
# Version: 1.0
# By: Yaniv Sharon
# endregion -------------Info------------

# region -------------Imports---------
import MemoryHandler
import time
import os
import Utility
# endregion -------------Imports---------

# region -------------Methods-----------


def header_maker(code, content_len='0', download_file=False, keep_connection=False, file_name=''):
    server_settings = MemoryHandler.get_server_settings()
    header = server_settings['version'] + ' ' + server_settings[code] + '\r\n'
    header_dict = {'Date': time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())}
    file_type = file_name.split('.')[-1]
    if file_type == 'txt':
        content_type = 'text/plain'
    elif file_type == 'html' or file_type == 'htm':
        content_type = 'text/html'
    elif file_type == 'pdf':
        content_type = 'application/pdf'
    elif file_type == 'exe':
        content_type = 'application/octet-stream'
    elif file_type == 'zip':
        content_type = 'application/zip'
    elif file_type == 'doc':
        content_type = 'application/msword'
    elif file_type == 'xls':
        content_type = 'application/vnd.ms-excel'
    elif file_type == 'ppt':
        content_type = 'application/vnd.ms-powerpoint'
    elif file_type == 'ico':
        content_type = 'image/x-icon'
    elif file_type == 'gif':
        content_type = 'image/gif'
    elif file_type == 'png':
        content_type = 'image/png'
    elif file_type == 'jpeg' or file_type == 'jpg':
        content_type = 'image/jpg'
    else:
        content_type = 'application/force-download'
    if download_file:
        header_dict['Content-disposition'] = 'attachment; filename=' + file_name
        header_dict['Pragma'] = 'public'
        header_dict['Expires'] = '0'
        header_dict['Cache-Control'] = 'private, must-revalidate, post-check=0, pre-check=0'
    header_dict['Content-Type'] = content_type + '; charset=UTF-8'
    header_dict['Content-Length'] = content_len
    if keep_connection:
        header_dict['Connection'] = 'keep'
    else:
        header_dict['Connection'] = 'close'
    for key in header_dict:
        header += key + ': ' + header_dict[key] + '\r\n'
    header += '\r\n'
    return header


def request_checker(request_dict):
    server_settings = MemoryHandler.get_server_settings()
    header_list = request_dict['header']
    if len(header_list) != 3 or header_list[2].split('/')[0] != server_settings['version'].split('/')[0]:
        return '400'
    if header_list[2].split('/')[1] != server_settings['version'].split('/')[1]:
        return '505'
    valid_type = False
    for request_type in server_settings['request_types'].split('/'):
        if header_list[0] == request_type:
            valid_type = True
    if not valid_type:
        return '501'
    return None


def get_response(request_dict, keep_connection, client_ip):
    parameter_dict = {}
    message = ''
    file_name = ''
    url = request_dict['header'][1].split('?')
    if url[0].startswith('/getfile') and len(url) == 2:
        parameters_list = url[1].replace(';', '&').split('&')
        for parameter in parameters_list:
            if len(parameter.split('=')) == 2:
                parameter_dict[parameter.split('=')[0]] = parameter.split('=')[1]
        if 'name' not in parameter_dict:
            return header_maker('400', keep_connection=False)
        file_name = parameter_dict['name'].replace('%20', ' ')
        file_password = ''
        if 'password' in parameter_dict:
            file_password = parameter_dict['password'].replace('%20', ' ')
        has_file, requested_file = MemoryHandler.hash_get_file(file_name, file_password)
        if has_file:
            file_text = requested_file.read()
            file_name = os.path.basename(requested_file.name)
            requested_file.close()
            print 'Sending the file "%s" to: %s' % (file_name, client_ip)
            return header_maker('200', content_len=str(len(file_text)), download_file=True, keep_connection=keep_connection, file_name=file_name) + file_text
        else:
            print 'Can`t get the file "%s" for: %s' % (file_name, client_ip)
            file_name = 'getfile.html'
            message = 'Wrong file name or password'
    if file_name == '':
        if url[0] == '/':
            file_name = 'index.html'
        elif url[0] == '/getfile':
            file_name = 'getfile.html'
        elif url[0] == '/uploadfile':
            file_name = 'uploadfile.html'
        elif url[0] == '/delfile':
            file_name = 'delfile.html'
        else:
            file_name = url[0][1:]
    file_found, file_data = MemoryHandler.get_server_file(file_name)
    if file_found:
        if file_name == 'getfile.html':
            file_data = Utility.add_to_mark(file_data, message)
        print 'Sending the server file "%s" to: %s' % (file_name, client_ip)
        return header_maker('200', content_len=str(len(file_data)), download_file=False, keep_connection=True, file_name=file_name) + file_data
    return header_maker('404', keep_connection=False)


def post_response(request_dict, keep_connection, client_ip):
    if request_dict['Content-Type'][0] != 'multipart/form-data':
        return header_maker('400', keep_connection=False)
    boundary = None
    for content_info in request_dict['Content-Type']:
        if content_info.startswith('boundary='):
            boundary = content_info[9:]
    if boundary is None:
        return header_maker('400', keep_connection=False)
    info_list = request_dict['body'].split('--' + boundary)
    info_list = info_list[1:-1]
    for index, item in enumerate(info_list):
        info_list[index] = item[2:-2]
    contents_dicts = [{} for thank_you_frenkel in range(len(info_list))]
    for info_num, info in enumerate(info_list):
        contents_dicts[info_num]['header'] = info.split('\r\n\r\n')[0]
        contents_dicts[info_num]['data'] = info.split('\r\n\r\n')[1]
    for item_num, item in enumerate(contents_dicts):
        header = item['header'].split('\r\n')
        for line in header:
            if line.startswith('Content-Disposition: form-data; '):
                variables = line[32:].split('; ')
                variables_dict = {}
                for variable in variables:
                    variables_dict[variable.split('=')[0]] = variable.split('=')[1][1:-1]
        contents_dicts[item_num].update(variables_dict)
    file_ending = None
    file_name = None
    file_password = None
    file_data = None
    for content in contents_dicts:
        if content['name'] == 'name':
            file_name = content['data']
        elif content['name'] == 'password':
            file_password = content['data']
        elif content['name'] == 'file':
            if len(content['filename'].split('.')) == 1:
                file_ending = ''
            else:
                file_ending = content['filename'].split('.')[-1]
            file_data = content['data']
    if file_name is None or Utility.all_chars(file_name.replace('%20', ' '), ' ') or file_data is None:
        return header_maker('400', keep_connection=False)
    if file_ending != '':
        file_name = '%s.%s' % (file_name, file_ending)
    if file_password is None:
        file_password = ''
    file_saved = MemoryHandler.hash_save_file(file_name, file_password, file_data)
    if file_saved:
        message = '<i>file saved, you can get it at:</i><br><u>http://%s/getfile?name=%s' % (MemoryHandler.get_server_settings()['domain'], file_name.replace(' ', '%20'))
        if file_password != '':
            message += '&password=' + file_password.replace(' ', '%20')
        message += '</u>'
    else:
        message = 'file not saved'
    got_file, replay_file = MemoryHandler.get_server_file('uploadfile.html')
    if not got_file:
        return header_maker('500', keep_connection=False)
    new_replay_text = Utility.add_to_mark(replay_file, message)
    return header_maker('200', content_len=str(len(new_replay_text)), download_file=False, keep_connection=keep_connection, file_name='uploadfile.html') + new_replay_text



def delete_response(request_dict, keep_connection):
    if request_dict['Content-Type'][0] != 'multipart/form-data':
        return header_maker('400', keep_connection=False)
    boundary = None
    for content_info in request_dict['Content-Type']:
        if content_info.startswith('boundary='):
            boundary = content_info[9:]
    if boundary is None:
        return header_maker('400', keep_connection=False)
    info_list = request_dict['body'].split('--' + boundary)
    info_list = info_list[1:-1]
    for index, item in enumerate(info_list):
        info_list[index] = item[2:-2]
    contents_dicts = [{} for thank_you_frenkel in range(len(info_list))]
    for info_num, info in enumerate(info_list):
        contents_dicts[info_num]['header'] = info.split('\r\n\r\n')[0]
        contents_dicts[info_num]['data'] = info.split('\r\n\r\n')[1]
    for item_num, item in enumerate(contents_dicts):
        header = item['header'].split('\r\n')
        for line in header:
            if line.startswith('Content-Disposition: form-data; '):
                variables = line[32:].split('; ')
                variables_dict = {}
                for variable in variables:
                    variables_dict[variable.split('=')[0]] = variable.split('=')[1][1:-1]
        contents_dicts[item_num].update(variables_dict)
    file_name = None
    file_password = None
    for content in contents_dicts:
        if content['name'] == 'name':
            file_name = content['data']
        elif content['name'] == 'password':
            file_password = content['data']
    if file_name is None:
        return header_maker('400', keep_connection=False)
    if file_password is None:
        file_password = ''
    deleted_file, message = MemoryHandler.hash_delete_file(file_name, file_password)
    got_file, replay_file = MemoryHandler.get_server_file('delfile.html')
    if not got_file:
        return header_maker('500', keep_connection=False)
    new_replay_text = Utility.add_to_mark(replay_file, message)
    return header_maker('200', content_len=str(len(new_replay_text)), download_file=False, keep_connection=keep_connection, file_name='uploadfile.html') + new_replay_text


def handle_request(request, client_ip):
    replay = ''
    request = request.split('\r\n\r\n', 1)
    if len(request) != 2:
        return False, header_maker('400', keep_connection=False)
    request_parameters_list = request[0].split('\r\n')
    request_dict = {'header': request_parameters_list[0].split(), 'body': request[1]}
    for parameter in request_parameters_list[1:]:
        if parameter != '':
            parameter = parameter.split(': ')
            request_dict[parameter[0]] = parameter[1].split('; ')
    check_results = request_checker(request_dict)
    if check_results is not None:
        keep_connection = False
        replay = header_maker(check_results, keep_connection=False)
    else:
        keep_connection = (request_dict['Connection'][0] == 'keep-alive')
        if request_dict['header'][0] == 'GET':
            replay = get_response(request_dict, keep_connection, client_ip)
        elif request_dict['header'][0] == 'POST':
            if request_dict['header'][1].startswith('/uploadfile'):
                replay = post_response(request_dict, keep_connection, client_ip)
            elif request_dict['header'][1].startswith('/delfile'):
                replay = delete_response(request_dict, keep_connection)
        else:
            replay = header_maker('501', keep_connection=True)
    return keep_connection, replay
# endregion -------------Methods-----------
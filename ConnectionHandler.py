# region -------------Info------------
# Name: connection handler
# Version: 1.0
# By: Yaniv Sharon
# endregion -------------Info------------

# region -------------Imports---------
import select
import socket
import MemoryHandler
import RequestHandler
# endregion -------------Imports---------

# region -------------Class-----------


class ConnectionHandler:
    def __init__(self):
        self.open_http_sockets = []
        self.open_https_sockets = []
        self.settings = MemoryHandler.get_server_settings()
        self.http_socket = socket.socket()
        self.http_socket.bind((self.settings['http_ip'], int(self.settings['http_port'])))
        self.http_socket.listen(10)
        self.https_socket = socket.socket()
        self.https_socket.bind((self.settings['https_ip'], int(self.settings['https_port'])))
        self.https_socket.listen(10)

    def http_communication(self, socket):
        print 'Got a request from: ' + socket.getpeername()[0]
        has_length = False
        content_length = 0
        data = socket.recv(int(self.settings['buff_size']))
        header_data = data.split('\r\n\r\n')[0]
        header_list = header_data.split('\r\n')
        for header in header_list:
            if header.startswith('Content-Length: '):
                content_length = int(header[16:])
                has_length = True
        good_download = True
        old_data_size = 0
        while len(data) - len(header_data + '\r\n\r\n') < content_length and has_length:
            data_size = len(data)
            request_size = len(header_data + '\r\n\r\n') + content_length
            percents = (float(data_size) / float(request_size)) * 100.0
            if data_size == old_data_size:
                good_download = False
                break
            old_data_size = data_size
            print 'Got %d out of %d/ %d' % (data_size, request_size, percents) + '%'
            data += socket.recv(int(self.settings['buff_size']))
        if good_download:
            try:
                keep_connection, replay = RequestHandler.handle_request(data, socket.getpeername()[0])
            except:
                keep_connection = False
                replay = RequestHandler.header_maker('500', keep_connection=False)
            if replay is not None:
                socket.send(replay)
        else:
            print 'The client stopped transferring the file'
            socket.send(RequestHandler.header_maker('400', keep_connection=False))
            keep_connection = False
        if not keep_connection:
            self.open_http_sockets.remove(socket)
            socket.close()
        return

    def https_communication(self, socket):
        data = socket.recv(int(self.settings['buff_size']))
        keep_connection, replay = RequestHandler.handle_request(data)
        socket.send(replay)
        if not keep_connection:
            self.open_https_sockets.remove(socket)
            socket.close()
        return

    def handle_connections(self):
        rlist, wlist, xlist = select.select([self.http_socket, self.https_socket] + self.open_http_sockets + self.open_https_sockets, [], [])
        for socket in rlist:
            if socket is self.http_socket:
                # handle the server http socket
                client, address = socket.accept()
                print 'Got a new connection from: ' + address[0]
                self.open_http_sockets.append(client)
            elif socket is self.https_socket:
                # handle the server https socket
                client, address = socket.accept()
                self.open_https_sockets.append(client)
            else:
                # handle all other http sockets
                if socket in self.open_http_sockets:
                    self.http_communication(socket)
                elif socket in self.open_https_sockets:
                    self.https_communication(socket)

# endregion -------------Class-----------
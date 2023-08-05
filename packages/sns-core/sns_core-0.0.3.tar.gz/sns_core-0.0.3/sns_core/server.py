import socket
import threading
import time

from .parser import parse, parse_content
from .objects import SNSinteraction
from .exceptions import SNSserverException

class SNSserver(object):

    HOST = '0.0.0.0'
    PORT = 3735

    components = {}

    server_thread = None
    conn_threads = []

    def __init__(self, type=None, action=None):
        self.type = type
        self.action = action

        if self.type is None:
            self.type = "*"

        if self.action is None:
            self.action = "*"

    def __call__(self, func):
        if not isinstance(self.type, list):
            self.type = [self.type]

        if not isinstance(self.action, list):
            self.action = [self.action]

        for type in self.type:
            for action in self.action:
                self.components[type, action] = func

    @staticmethod
    def start_server():
        SNSserver.server_thread = threading.Thread(target=SNSserver.server_thread)
        SNSserver.server_thread.start()

    @staticmethod
    def server_thread():
        print("Starting on:", SNSserver.HOST, SNSserver.PORT)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((SNSserver.HOST, SNSserver.PORT))
        s.listen(1)

        print("Server has started..")

        while True:
            conn, addr = s.accept()

            conn_thread = threading.Thread(target=SNSserver.connection_handler, args=(conn, addr))
            conn_thread.start()
            
            SNSserver.conn_threads.append(conn_thread)

        s.close()

    @staticmethod
    def connection_handler(conn, addr):
        with conn:
            print('Connected with', addr)
            conn.settimeout(2)
            while True:
                try:
                    data = b''
                    count = 0

                    while True:
                        temp_data = conn.recv(5120)
                        if (len(temp_data) < 1): break
                        time.sleep(0.2)
                        count = count + len(temp_data)
                        data += temp_data

                    interaction_blobs = data.split(b'\r\n\r\n')

                    interactions = []
                    for interaction_blob in interaction_blobs:
                        try:
                            interaction = parse(interaction_blob)
                        except:
                            if len(interactions) > 0:
                                interactions[-1].content.append(interaction_blob)
                            else:
                                raise SNSserverException()

                    print(addr, "Received interaction:")
                    print(interaction_object)

                    if (interaction_object.type, interaction_object.action) in SNSserver.components:
                        response = SNSserver.components[interaction_object.type, interaction_object.action](interaction_object)
                    elif (interaction_object.type, "*") in SNSserver.components:
                        response = SNSserver.components[interaction_object.type, "*"](interaction_object)
                    elif ("*", interaction_object.action) in SNSserver.components:
                        response = SNSserver.components["*", interaction_object.action](interaction_object)
                    elif ("*", "*") in SNSserver.components:
                        response = SNSserver.components["*", "*"](interaction_object)
                    else:
                        print(addr, "Interaction component not found")
                        response = SNSinteraction("STATUS", 404, {'From':interaction_object.headers['To'], 'To':interaction_object.headers['From']})

                    print(addr, "Constructed response:")
                    if isinstance(response, list):
                        if len(response) == 0:
                            response = SNSinteraction("STATUS", 401, {'From':interaction_object.headers['To'], 'To':interaction_object.headers['From']})
                            print(response.type, response.action)
                            print(response.headers)
                            conn.sendall(response.to_bytes())
                        else:
                            print('\n'.join([item.type + ' ' + item.action + '\n' + item.headers for item in response]))
                            conn.sendall(b'\r\n\r\n'.join([item.to_bytes() for item in response]))
                    else:
                        print(response.type, response.action)
                        print(response.headers)
                        conn.sendall(str(response).encode("utf-8"))
                except socket.error:
                    print("[WARNING] Something was wrong with the socket connection, further investigation is needed if this issue persists")
                    break
                except SNSserverException:
                    print("[WARNING] A server exception occured, meaning something went wrong with loading in or sending a request")
                    break
        conn.close()
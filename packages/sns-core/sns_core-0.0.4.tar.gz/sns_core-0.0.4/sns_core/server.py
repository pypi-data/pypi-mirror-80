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
                    buffer_size = 4096
                    data = b''

                    while True:
                        temp_data = conn.recv(buffer_size)
                        data += temp_data
                        if (len(temp_data) < buffer_size): break
                        time.sleep(0.2)

                    if len(data) == 0:
                        break

                    interaction_blobs = data.split(b'\r\n\r\n')

                    interactions = []
                    for interaction_blob in interaction_blobs:
                        try:
                            interactions.append(parse(interaction_blob))
                        except:
                            if len(interactions) > 0:
                                interactions[-1].content.append(interaction_blob)
                            else:
                                raise SNSserverException()

                    print(addr, "Received interaction:")
                    print(interactions)

                    responses = []

                    for interaction_object in interactions:
                        response = None
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

                        if response is None:
                            continue
                        elif isinstance(response, list):
                            responses += response
                        else:
                            responses.append(response)

                    if len(responses) == 0:
                        raise SNSserverException()

                    print(addr, "Constructed response:")
                    if len(responses) == 0:
                        response = SNSinteraction("STATUS", 401, {'From':responses[0].headers['To'], 'To':responses[1].headers['From']})
                        print(response.type, response.action)
                        print(response.headers)
                        conn.sendall(response.to_bytes())
                    elif len(responses) == 1:
                        response = responses[0]
                        print(response.type, response.action)
                        print(response.headers)
                        conn.sendall(response.to_bytes())
                    else:
                        print('\n'.join([item.type + ' ' + item.action + '\n' + item.headers for item in responses]))
                        conn.sendall(b'\r\n\r\n'.join([item.to_bytes() for item in responses]))

                except socket.error:
                    print("[WARNING] Something was wrong with the socket connection, further investigation is needed if this issue persists")
                    break
                except SNSserverException as e:
                    print(e)
                    print("[WARNING] A server exception occured, meaning something went wrong with loading in or sending a request")
                    break
        conn.close()
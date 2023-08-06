from .parser import parse
from .exceptions import SNSinteractionException, SNSserverException
from .records import get_user_record
from .objects import SNSinteraction, SNScontent

import socket
import re

SNS_PORT = 3735

#TODO: encrypt the whole request with the private key of the user first, to ensure integrity and authenticity. 
#Since the public key is already known to the server, this does not require any extra steps either.
def request(type, action, content=None, **headers):
    for key, value in headers.items():
        try:
            headers[key] = str(value)
        except IndexError:
            raise SNSinteractionException(str(headers), "One of the interaction headers could not be parsed to a string")

    interaction = parse(str(SNSinteraction(type, action, headers, content)))

    if interaction.headers['To'].count('@') > 1:
        raise SNSinteractionException(str(interaction), "The To header contains too many @ characters (max. 1 per address header), causing that the address cannot be determined")

    try:
        address = interaction.headers['To'].split('@')[1]
    except:
        address = get_user_record().provider

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((address, SNS_PORT))
    conn.sendall(str(interaction).encode('utf-8'))

    buffer_size = 4096
    data = b''

    while True:
        temp_data = conn.recv(buffer_size)
        data += temp_data
        if (len(temp_data) < buffer_size): break
        time.sleep(0.2)

    conn.close()

    interaction_blobs = re.split(r"(?:\r?\n){2,}", data.decode('utf-8'))

    interactions = []
    for interaction_blob in interaction_blobs:
        try:
            interactions.append(parse(interaction_blob))
        except:
            if len(interactions) > 0:
                interactions[-1].content.append(interaction_blob)
            else:
                raise SNSserverException()
    
    return interactions

def user(action, To, content=None, **headers):
    encrypted_content = content

    headers['From'] = 'user:' + get_user_record().identifier
    headers['To'] = To

    interaction_object = request('USER', action, encrypted_content, **headers)
    
    return interaction_object

def group(action, To, content=None, **headers):
    encrypted_content = content

    headers['From'] = 'user:' + get_user_record().identifier
    headers['To'] = To

    interaction_object = request('GROUP', action, encrypted_content, **headers)
    
    return interaction_object

def post(action, To, content=None, **headers):
    encrypted_content = content

    headers['From'] = 'user:' + get_user_record().identifier
    headers['To'] = To

    interaction_object = request('POST', action, encrypted_content, **headers)
    
    return interaction_object

def reaction(action, To, content=None, **headers):
    encrypted_content = content

    headers['From'] = 'user:' + get_user_record().identifier
    headers['To'] = To

    interaction_object = request('REACTION', action, encrypted_content, **headers)
    
    return interaction_object
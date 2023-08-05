from .parser import parse
from .exceptions import SNSinteractionException
from .records import SNSuserRecord
from .objects import SNSinteraction, SNScontent

import socket

SNS_PORT = 3735

#TODO: encrypt the whole request with the private key of the user first, to ensure integrity and authenticity. 
#Since the public key is already known to the server, this does not require any extra steps either.
def request(type, action, content=None, **headers):
    for key, value in headers.items():
        try:
            headers[key] = str(value)
        except IndexError:
            raise SNSinteractionException(str(headers), "One of the interaction headers could not be parsed to a string")

    interaction = parse(SNSinteraction(type, action, headers, content).to_bytes())

    if interaction.headers['To'].count('@') > 1:
        raise SNSinteractionException(str(interaction), "The To header contains too many @ characters (max. 1 per address header), causing that the address cannot be determined")

    try:
        address = interaction.headers['To'].split('@')[1]
    except:
        address = SNSuserRecord.provider

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((address, SNS_PORT))
    conn.sendall(interaction.to_bytes())

    buffer_size = 4096
    data = b''

    while True:
        temp_data = conn.recv(buffer_size)
        data += temp_data
        if (len(temp_data) < buffer_size): break
        time.sleep(0.2)

    conn.close()

    interaction_blobs = data.split(b'\r\n\r\n')

    interactions = []
    for interaction_blob in interaction_blobs:
        try:
            interaction = parse(interaction_blob)
        except:
            if len(interactions) > 0:
                interactions[-1].content.append(interaction_blob)
    
    return interactions

def user(action, To, content=None, **headers):
    encrypted_content = content

    headers['From'] = 'user:' + SNSuserRecord.identifier
    headers['To'] = To

    interaction_object = request('USER', action, encrypted_content, **headers)
    
    return interaction_object

def group(action, To, content=None, **headers):
    encrypted_content = content

    headers['From'] = 'user:' + SNSuserRecord.identifier
    headers['To'] = To

    interaction_object = request('GROUP', action, encrypted_content, **headers)
    
    return interaction_object

def post(action, To, content=None, **headers):
    encrypted_content = content

    headers['From'] = 'user:' + SNSuserRecord.identifier
    headers['To'] = To

    interaction_object = request('POST', action, encrypted_content, **headers)
    
    return interaction_object

def reaction(action, To, content=None, **headers):
    encrypted_content = content

    headers['From'] = 'user:' + SNSuserRecord.identifier
    headers['To'] = To

    interaction_object = request('REACTION', action, encrypted_content, **headers)
    
    return interaction_object
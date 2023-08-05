from .parser import SNSinteraction, parse
from .exceptions import SNSinteractionException
from .records import SNSuserRecord

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

    interaction = parse(str(SNSinteraction(type, action, headers, content)))

    if interaction.headers['To'].count('@') > 1:
        raise SNSinteractionException(str(interaction), "The To header contains too many @ characters (max. 1 per address header), causing that the address cannot be determined")

    try:
        address = interaction.headers['To'].split('@')[1]
    except:
        address = SNSuserRecord.provider

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, SNS_PORT))
    s.sendall(str(interaction).encode())
    data = s.recv(4096)
    s.close()

    interaction_strings = data.decode("utf-8").split("\n\n")
    interaction_strings = ["\n\n".join(interaction_strings[i:i+2]) for i in range(0, len(interaction_strings), 2)]
    
    return [parse(interaction_string) for interaction_string in interaction_strings]

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
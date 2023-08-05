from .exceptions import SNSobjectException
from .parser import parse_content

class SNSinteraction:

    def __init__(self, type, action, headers={}, content=None):
        self.type = str(type)
        self.action = str(action)
        self.headers = headers
        self.content = SNScontent(content)

    def get(self, key, default=None):
        return self.headers.get(key, default)

    def to_bytes(self):
        interaction_string = self.type + " " + self.action

        if len(self.headers) > 0:
            interaction_string += '\r\n'
            interaction_string += '\r\n'.join(header[0] + ": " + header[1] for header in self.headers)

        return interaction_string.decode('utf-8') + '\r\n\r\n' + self.content.to_bytes()

class SNScontent:

    def __init__(self, content=None):
        self.__decrypted_content = []
        self.__encrypted_content = []
        self.__attachments = []

        if type(content) == str:
            # try to parse, since it's probably decrypted content
            parsed_content = parse_content(content)
            if isinstance(parsed_content, dict):
                self.__decrypted_content.append(parsed_content)
        elif isinstance(content, dict):
            # decrypted content
            self.__decrypted_content.append(content)
        elif type(content) == bytes:
            # could be encrypted content, by parsing we can find out
            if content.startswith(b'Attachment: '):
                self.__attachments.append(content[len(b'Attachment: '):])
            else:
                self.__encrypted_content.append(content)            
        elif type(content) == SNScontent:
            # somehow we got an SNScontent object, just unpack and add to this class
            self.__decrypted_content = content.get_decrypted_content()
            self.__encrypted_content = content.get_encrypted_content()
            self.__attachments = content.get_attachments()

    def get_decrypted_content(self):
        return self.__decrypted_content

    def get_encrypted_content(self):
        return self.__encrypted_content

    def get_attachments(self):
        return self.__attachments

    def to_bytes(self):
        decrypted_bytes = b'\r\n'.join([(key + ': ' + value).encode('utf-8') for key, value in self.__decrypted_content.items()])

        encrypted_bytes = b'\r\n'.join(self.__encrypted_content)

        attachments_bytes = b'\r\n'.join(self.__attachments)

        return decrypted_bytes + b'\r\n\r\n' + encrypted_bytes + '\r\n\r\n' + attachments_bytes
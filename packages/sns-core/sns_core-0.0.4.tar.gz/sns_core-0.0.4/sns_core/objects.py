from .exceptions import SNSobjectException

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
            interaction_string += '\r\n'.join([header[0] + ": " + str(header[1]) for header in self.headers.items()])

        content_bytes = self.content.to_bytes()

        if len(content_bytes) > 0:
            return interaction_string.encode('utf-8') + b'\r\n\r\n' + content_bytes
        else:
            return interaction_string.encode('utf-8')

class SNScontent:

    def __init__(self, content=None):
        self.__decrypted_content = []
        self.__encrypted_content = []
        self.__attachments = []

        if isinstance(content, list):
            for item in content:
                self.set_content(item)
        else:
            self.set_content(content)


    def set_content(self, content):
        if type(content) == str:
            # try to parse, since it's probably decrypted content
            try:
                content_parameters = content.splitlines()
                parsed_content = {}

                for content_parameter in content_parameters:
                    param_type, param_value = content_parameter.split(": ")

                    parsed_content[param_type] = param_value

                self.__decrypted_content.append(parsed_content)
            except:
                raise SNSobjectException(content, "Content was passed as a str, but could not be parsed to a dict")
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
        result_bytes = b'\r\n\r\n'.join([b'\r\n'.join([(key + ': ' + value).encode('utf-8') for key, value in item.items()]) for item in self.__decrypted_content]) 

        if len(self.__encrypted_content) > 0:
            result_bytes += b'\r\n\r\n' + b'\r\n'.join(self.__encrypted_content)

        if len(self.__attachments) > 0:
            result_bytes += b'\r\n\r\n' + b'\r\n'.join([b'Attachment: ' + attachment for attachment in self.__attachments])

        return result_bytes
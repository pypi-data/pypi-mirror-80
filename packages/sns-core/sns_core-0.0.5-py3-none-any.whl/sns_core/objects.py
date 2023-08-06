from .exceptions import SNSobjectException

class SNSinteraction:

    def __init__(self, type, action, headers={}, content=None):
        self.type = str(type)
        self.action = str(action)
        self.headers = headers
        self.content = SNScontent(content)

    def get(self, key, default=None):
        return self.headers.get(key, default)

    def __str__(self):
        interaction_string = self.type + " " + self.action

        if len(self.headers) > 0:
            interaction_string += '\r\n'
            interaction_string += '\r\n'.join([header[0] + ": " + str(header[1]) for header in self.headers.items()])

        content_string = str(self.content)

        if len(content_string) > 0:
            return interaction_string + '\r\n\r\n' + content_string
        else:
            return interaction_string

class SNScontent:

    def __init__(self, content=None):
        self.content = []

        self.append(content)

    def append_list(self, content):
        for item in content:
            self.append(item)

    def append(self, content):
        if type(content) == str:
            # try to parse, since it's probably decrypted content
            try:
                content_parameters = content.splitlines()
                _interaction_content = {}

                for content_parameter in content_parameters:
                    param_type, param_value = content_parameter.split(": ")

                    if param_type in _interaction_content:
                        _interaction_content[param_type] = [_interaction_content[param_type], param_value]
                    else:
                        _interaction_content[param_type] = param_value

                self.content.append(_interaction_content)
            except:
                raise SNSobjectException(content, "Content was passed as a str, but could not be parsed to a dict")
        elif isinstance(content, dict):
            # decrypted content
            self.content.append(content)
        elif type(content) == bytes:
            # could be encrypted content, by parsing we can find out
            self.append(content.decode('utf-8'))
        elif type(content) == SNScontent:
            # somehow we got an SNScontent object, just unpack and add to this class
            self.append_list(content.content)
        elif isinstance(content, list):
            self.append_list(content)

    def get(self, key, default=None):
        for item in self.content:
            result = item.get(key, default)
            if result is not None and result is not default:
                return result
        return default

    def __str__(self):
        return '\r\n\r\n'.join(['\r\n'.join([(key + ': ' + value) for key, value in item.items()]) for item in self.content]) 
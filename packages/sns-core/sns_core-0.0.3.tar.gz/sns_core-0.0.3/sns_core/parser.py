import re

from .exceptions import SNSparserException
from .objects import SNSinteraction, SNScontent            

def parse(interaction):
    """
    Parses a string representing a interaction made with the SNS protocol.
    """
    try:
        interaction = interaction.decode('utf-8')
        raise AttributeError()
    except AttributeError:
        interaction.replace('\r\n', '\n')

    interaction_lines = interaction.split('\n\n')
    headers = interaction_lines[0].splitlines()

    if len(interaction_lines) > 2:
        raise SNSparserException(interaction, 'The interaction has two empty lines, while only one after the headers is allowed')

    try:
        interaction_method = headers[0]
    except IndexError:
        raise SNSparserException(interaction, 'The interaction method cannot be parsed, missing the first line')

    try:
        _interaction_type, _interaction_action = interaction_method.split(" ")

        if len(_interaction_type) == 0:
            raise SNSparserException(interaction_method, 'The interaction type is empty')

        if not _interaction_type.isupper():
            raise SNSparserException(interaction_method, 'The interaction type is not capitalized, suggesting it is not a proper interaction type')

        if len(_interaction_action) == 0:
            raise SNSparserException(interaction_method, 'The interaction action is empty')

        if not _interaction_action.islower() and re.match(r'^-?\d+(?:\.\d+)?$', _interaction_action) is None:
            raise SNSparserException(interaction_method, 'The interaction action contains capitalized letters, suggesting it is not a proper interaction action')
    except ValueError:
        raise SNSparserException(interaction_method, 'The interaction method does not contain the interaction type and action')

    header_fields = headers[1:]
    _interaction_headers = {}
    
    for header_field in header_fields:
        try:
            header_type, header_value = header_field.split(': ')

            if len(header_type) == 0:
                raise SNSparserException(header_field, 'The header type is empty')

            if len(header_value) == 0:
                raise SNSparserException(header_field, 'The header value is empty')

            if header_type in _interaction_headers.keys():
                raise SNSparserException(header_field, 'This header type is a duplicate and is already set')

            _interaction_headers[header_type] = header_value
        except ValueError:
            raise SNSparserException(header_field, 'The header field does not contain a type and value')

    if "From" not in _interaction_headers.keys():
        raise SNSparserException(headers, 'The interaction is missing the From field, make sure this is set as a header')

    if not len(_interaction_headers['From'].split(":")) == 2:
        raise SNSparserException(headers, 'The identifier in the From header is missing an interaction qualifier, e.g. \'user\' or \'group\'')

    if "To" not in _interaction_headers.keys():
        raise SNSparserException(headers, 'The interaction is missing the To field, make sure this is set as a header')

    if not len(_interaction_headers['To'].split(":")) == 2:
        raise SNSparserException(headers, 'The identifier in the To header is missing an interaction qualifier, e.g. \'user\' or \'group\'')

    _interaction_content = None
    if len(interaction_lines) == 2 and len(interaction_lines[1]) > 0:
        _interaction_content = parse_content(interaction_lines[1])

    return SNSinteraction(_interaction_type, _interaction_action, _interaction_headers, _interaction_content)

def parse_content(content):
    try:
        content_parameters = content.splitlines()
        _interaction_content = {}

        for content_parameter in content_parameters:
            param_type, param_value = content_parameter.split(": ")

            _interaction_content[param_type] = param_value
    except:
        _interaction_content = content

    return _interaction_content
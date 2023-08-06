import unittest

from .parser import parse, SNSinteraction
from .exceptions import SNSparserException

class TestSNSParser(unittest.TestCase):

    def test_parse_user_follow(self):
        interaction = """USER follow
From: user:alice@snsprovider.net
To: user:bob@snsservice.com"""
        
        interaction_object = parse(interaction)
        assert not interaction_object == None
        assert interaction_object.type == "USER"
        assert interaction_object.action == "follow"
        assert interaction_object.headers == {'From':'user:alice@snsprovider.net','To':'user:bob@snsservice.com'}
        assert interaction_object.content is None

    def test_parse_empty(self):
        self.assertRaisesRegex(SNSparserException, 
        'The interaction method cannot be parsed, missing the first line', parse, '')

    def test_parse_missing_type(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The interaction type is empty', parse, ' follow')

    def test_parse_missing_action(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The interaction action is empty', parse, 'USER ')

    def test_parse_lower_type(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The interaction type is not capitalized, suggesting it is not a proper interaction type', parse, 'uSeR follow')

    def test_parse_upper_action(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The interaction action contains capitalized letters, suggesting it is not a proper interaction action', parse, 'USER Follow')

    def test_parse_with_content(self):
        interaction = """POST create
From: user:alice@snsprovider.net
To: user:bob@snsservice.com

Hello"""
        
        interaction_object = parse(interaction)
        assert not interaction_object == None
        assert interaction_object.type == "POST"
        assert interaction_object.action == "create"
        assert interaction_object.headers == {'From':'user:alice@snsprovider.net','To':'user:bob@snsservice.com'}
        assert interaction_object.content == "Hello"

    def test_double_parse(self):
        interaction = """POST create
From: user:alice@snsprovider.net
To: user:bob@snsservice.com
Limit: 3
Do: 5

Hello"""
        
        interaction_object = parse(interaction)
        assert not interaction_object == None
        assert interaction_object.type == "POST"
        assert interaction_object.action == "create"
        assert interaction_object.headers == {'From':'user:alice@snsprovider.net','To':'user:bob@snsservice.com', 'Limit':'3', 'Do':'5'}
        assert interaction_object.content == "Hello"
        
        interaction_object = parse(str(interaction_object))
        assert not interaction_object == None
        assert interaction_object.type == "POST"
        assert interaction_object.action == "create"
        assert interaction_object.headers == {'From':'user:alice@snsprovider.net','To':'user:bob@snsservice.com', 'Limit':'3', 'Do':'5'}
        assert interaction_object.content == "Hello"

    def test_parse_content_no_break(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The header field does not contain a type and value', parse, """POST create
From: alice@snsprovider.net
To: bob@snsservice.com
Hello""")

    def test_content_two_breaks(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The interaction has two empty lines, while only one after the headers is allowed', parse, """POST create
From: alice@snsprovider.net
To: bob@snsservice.com

Hello

Hello again""")

    def test_missing_type_or_action(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The interaction method does not contain the interaction type and action', parse, 'USER')

    def test_too_many_types_or_actions(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The interaction method does not contain the interaction type and action', parse, 'USER follow unfollow')

    def test_missing_header_type(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The header type is empty', parse, """USER follow
: alice?""")

    def test_missing_header_value(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The header value is empty', parse, """USER follow
To: """)

    def test_invalid_header_field(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The header field does not contain a type and value', parse, """USER follow
To:ss""")

    def test_too_many_header_items(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The header field does not contain a type and value', parse, """USER follow
To: alice: or bob""")

    def test_missing_from_header(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The interaction is missing the From field, make sure this is set as a header', parse, """USER follow
To: alice""")

    def test_missing_to_header(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The interaction is missing the To field, make sure this is set as a header', parse, """USER follow
From: user:alice""")

    def test_header_duplicate(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: This header type is a duplicate and is already set', parse, """USER follow
From: alice
From: Bob""")

    def test_from_header_missing_qualifier(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The identifier in the From header is missing an interaction qualifier, e.g. \'user\' or \'group\'', parse, """USER follow
From: alice
To: user:Bob""")

    def test_to_header_missing_qualifier(self):
        self.assertRaisesRegex(SNSparserException, 
        '.*: The identifier in the To header is missing an interaction qualifier, e.g. \'user\' or \'group\'', parse, """USER follow
From: user:alice
To: Bob""")

if __name__ == '__main__':
    unittest.main()
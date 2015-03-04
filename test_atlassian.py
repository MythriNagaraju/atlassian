from atlassian import Tokenizer, Token, Mentions, Links,Emoticons
import unittest
import json

# emoticon - test rejects ASCII strings longer than 15 chars
# pass empty string to tokenizer, returns empty json string
# 
class TestMentions(unittest.TestCase):
    def setUp(self):
        self.valid_mentions = ["@chris","@chris878787"]
        self.invalid_mentions= ["%^9898@chris", "@@@@adam"]

    def test_valid_mentions(self):
        """
        Assert Mentions instances are created for valid 
        mentions
        """
        for mentions in self.valid_mentions:
            m = Mentions(mentions)
            m.process_token()
            self.assertTrue(m.result)

    def test_invalid_mentions(self):
        """
        Mentions should not be instantiated for invalid
        strings
        """
        for mentions in self.invalid_mentions:
            m = Mentions(mentions)
            m.process_token()
            self.assertFalse(m.result)

class TestEmoticons(unittest.TestCase):
    # "(cof(ab$dr)fee)" not working as intended 
    def setUp(self):
        self.valid_emoticons = ["(megusta)","abcd$r(coffee)","(cof(ab)fee)"]
        self.invalid_emoticons = ["(meg$$#@sta)", "(cof(%$3425)fee)"]

    def test_valid_emoticons(self):
        """
        Assert Emoticons instances are created for valid 
        emoticons
        """
        for em in self.valid_emoticons:
            e = Emoticons(em)
            e.process_token()
            self.assertTrue(e.result)

    def test_invalid_emoticons(self):
        """
        Emoticons should not be instantiated for invalid
        strings
        """
        for em in self.invalid_emoticons:
            e = Emoticons(em)
            e.process_token()
            self.assertFalse(e.result)

class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.test_only_mentions = "@Thomas what's up"
        self.test_only_emoticons = "(awesome)"
        self.empty_string = ""
        self.test_contains_all_tokens = "@bob @john (success) https://twitter.com/jdorfman/status/430511497475670016"

    def test_result_contains_mentions_only(self):
        """
        resulting json string should have only mentions
        """
        tokenizer = Tokenizer(self.test_only_mentions)
        result_json_string = tokenizer.generate_result()
        result_dict = json.loads(result_json_string)
        self.assertIn('mentions', result_dict.keys()) 
        self.assertNotIn('emoticons', result_dict.keys()) 
        self.assertNotIn('links', result_dict.keys()) 

    def test_result_contains_emoticons(self):
        """
        resulting json string should have only emoticons
        """
        tokenizer = Tokenizer(self.test_only_emoticons)
        result_json_string = tokenizer.generate_result()
        result_dict = json.loads(result_json_string)
        self.assertIn('emoticons', result_dict.keys()) 
        self.assertNotIn('mentions', result_dict.keys()) 
        self.assertNotIn('links', result_dict.keys()) 

if __name__ == '__main__':
    unittest.main()

import re
from urlparse import urlparse
import json
import urllib2
from BeautifulSoup import BeautifulSoup
import sys
from collections import defaultdict

#Mention class is taking caret
#Link is taking too long?
#link without http not being considered
#mention assumptions
#

class Token(object):
    def __init__(self, input):
        self.input = input
        self.result = None
        self.regex_pattern = None
        self.match = None

    def validate_token(self):
        match = re.search(self.regex_pattern, self.input)
        if match:
            self.match = match.group()
            return True

    def process_token(self):
        pass
        
class Mentions(Token):
    def __init__(self,input):
        super(Mentions, self).__init__(input)
        self.regex_pattern = '^@[^\^][a-zA-z]+'

    def process_token(self):
        if self.validate_token():
           self.result = self.match.strip('@')
         
class Links(Token):
    def process_token(self):
        try:
	    #open URL and get title from the header
	    page = urllib2.urlopen(self.input)
	    page_source = BeautifulSoup(page.read())        
	    title = page_source.html.head.title.renderContents() 
	    self.result = dict(zip(['url','title'],[self.input,title]))
        except:
            pass

class Emoticons(Token):
    def __init__(self,input):
        super(Emoticons, self).__init__(input)
        self.regex_pattern = '\([a-z]{1,15}\)'

    def process_token(self):
        # remove parentheses
        if self.validate_token():
            self.result = re.sub(r'[()]','',self.match)

class Tokenizer:
    def __init__(self,input):
        # Splits string and creates instances of
        # class Token
        strings = input.split(' ')
        self.json = defaultdict(list)
        self.tokens = []
        self.create_tokens(strings)

    def create_tokens(self,strings):
        # Validates each string and creates 
        # one of allowed tokens
	for string in strings:
            token = None
	    if '@' in string:
            # cursory check to see if this token
            # is a mention
                token = Mentions(string)
	    elif '(' in string and ')' in string:
            # cursory check to see if this token
            # is a Emoticon
                token = Emoticons(string)
	    else:
		# validate Url
		parse_result = urlparse(string)
		if parse_result.scheme:
		    token = Links(string)
            if token:
                token.process_token()
                if token.result:
                    self.json[token.__class__.__name__.lower()]\
                        .append(token.result)
    
    def generate_result(self):
        return json.dumps(self.json) 
    
def main():
    input = sys.argv[1]
    tokenizer = Tokenizer(input)
    print(tokenizer.generate_result())

if __name__=='__main__': main()
    

Assumptions
===========
1. Only word characters (i.e. a-z and A-z) within parantheses is considered to be an emoticon
   (ASCII non-word characters like #,$, or parantheses within parantheses are not considered 
   an emoticon)
2. Anything beginning with '@' only is considered to be a mention. For example '#$$^Abc@chris'
   is not a valid mention but '@chris' is
3. Only a URL with "http" scheme is considered a valid URL

How to run
==========
1. pip install requirements.txt
2. python atlassian.py <<input_string>>

To run tests
============
python test_atlassian.py

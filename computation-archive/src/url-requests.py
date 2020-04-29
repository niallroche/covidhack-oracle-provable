#!/usr/bin/python

import ast
import requests
import os

"""
The Smart Contract caller can pass in data to be processed, this can be urls to fetch and required headers and parameters

additional named parameters for post processing could be specified too to make this code more generic 
These could be a set of regular expressions or parse rules to post-process the data 
need to be careful that any of the params passed will not be an issue for the requests lib or for the url called
"""

# parse env args
arg = [os.environ['ARG0'], os.environ['ARG1']]

# parse 3rd arg into kwargs if available
if 'ARG2' in os.environ: kwargs = ast.literal_eval(os.environ['ARG2'])
else: kwargs = {}

# attempt the request
req = requests.request(arg[0], arg[1], **kwargs)

# check if post processor params were included

# print text result on single line
print(req.text.replace('\n',''))

# option if always json
# print(json.loads(req.text))

"""
MIT License

Copyright (c) 2020 Niall Roche

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

utility class to interface with IPFS
"""

from boto3 import client as boto3_client
from datetime import datetime
import json


def pin_json_to_ipfs(json_content):
    return lambda_handler(json_content, True)


def pin_content_to_ipfs(content):
    return lambda_handler(content)


def lambda_handler(content, is_json=True):
    lambda_client = boto3_client('lambda')
    print('in lambda_handler')
    print(json.dumps(content))

    if is_json:
        content = json.dumps(content)
    invoke_response = lambda_client.invoke(FunctionName="dev-save_to_ipfs",
                                           # InvocationType='Event',
                                           InvocationType='RequestResponse',
                                           Payload=content)
                                           # Payload=json.dumps(msg))
    print(invoke_response)
    if invoke_response['Payload'] is not None:
        data = invoke_response['Payload'].read().decode()
        return data
    else:
        return invoke_response

"""
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

# -*- coding: utf-8 -*-

__author__ = "Walter Hernandez"
__copyright__ = "Copyright 2020"
__credits__ = ["Niall Roche"]
__license__ = "MIT License"
__version__ = "1.0"
__summary__ = "Prepares Metadata of published datasets"

from datetime import datetime
import requests
import json

def generate_metadata_dict(response, metadata_dict=None, gateway_host="https://ipfs.io"):

    def get_content_type(url, type_url=None, gateway_host="https://ipfs.io"):
        # Convert to the right url to fetch the content type
        if type_url is not None:
            if "ipfs" in type_url:
                url = "/".join((gateway_host, type_url, url))

        # Get the content type returned from the headers of an url
        res = requests.get(url)
        content_type = res.headers['content-type']
        if ";" in content_type:
            content_type = content_type.split(";")[0]

        return content_type

    # Generates metadata dictionary for the first time if it is not an update to an existing one
    # Populates the metadata_dict with the static information
    if metadata_dict is None:
        metadata_dict = {"main": {
            "type": "dataset",
            "name": "COVID-19 UK Gov Dataset",
            "dateCreated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "author": "Mishcon de Reya LLC",
            "license": "CC0: Public Domain Dedication",
            "price": "0",
            "files": [],
            # Adds an initial datePublished, which would would be updated with each new file added to the list "files"
            "datePublished": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            },
            "additionalInformation": {
                "description": "Data files related to UK deaths and cases related to COVID-19, containing raw data available from uk gov and processed data files into a data schema usable by smart contracts",
                "copyrightHolder": "Mishcon de Reya LLC",
                "categories": ["Health"]
            }
        }
    if response:
        if type(response) == dict:
            if "IpfsHash" in response.keys():
                posted = {"contentType": get_content_type(response['IpfsHash'],
                                                          type_url="ipfs",
                                                          gateway_host=gateway_host),
                          "contentLength": response['PinSize'],
                          "compression": "plain",
                          "index": 0,
                          "url":"ipfs://" + response['IpfsHash']}

                metadata_dict["main"]['files'].append(posted)

        elif type(response) == str:
            if "http" in response:
                posted = {"contentType": get_content_type(response),
                          "url": response}

                metadata_dict["main"]['files'].append(posted)

    # Update the publish date of the metadata dictionary
    metadata_dict["main"]["datePublished"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    return metadata_dict
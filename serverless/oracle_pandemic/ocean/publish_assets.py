# -*- coding: utf-8 -*-

# Standard imports
import json
import logging
import os
from pathlib import Path
from time import sleep

# Import mantaray and the Ocean API (squid)
import random
import squid_py
from mantaray_utilities.user import create_account
from ocean_keeper.web3_provider import Web3Provider
from ocean_utils.did import did_to_id
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
from mantaray_utilities import logging as manta_logging, config

# Metadata
from serverless.oracle_pandemic.ocean.get_metadata import generate_metadata_dict

from pprint import pprint
""" 
1) Connect to the Ocean Protocol API
"""
# Setup logging
manta_logging.logger.setLevel('INFO')
print("squid-py Ocean API version:", squid_py.__version__)

# Get the configuration file path for this environment
OCEAN_CONFIG_PATH = Path(os.path.expanduser(os.environ['OCEAN_CONFIG_PATH']))
assert OCEAN_CONFIG_PATH.exists(), "{} - path does not exist".format(OCEAN_CONFIG_PATH)

logging.critical("Configuration file selected: {}".format(OCEAN_CONFIG_PATH))
logging.critical("Deployment type: {}".format(config.get_deployment_type()))
logging.critical("Squid API version: {}".format(squid_py.__version__))

# Instantiate Ocean with the default configuration file.
configuration = Config(OCEAN_CONFIG_PATH)
squid_py.ConfigProvider.set_config(configuration)
ocn = Ocean(configuration)
faucet_url = ocn.config.get('keeper-contracts', 'faucet.url')

""" 
2) Set up publisher account in Ocean
"""

# Get a publisher account
publisher_acct = create_account(faucet_url, wait=True)
print("Publisher account address: {}".format(publisher_acct.address))
print("Publisher account 'ETH' balance: {:>6.1f}".format(ocn.accounts.balance(publisher_acct).eth/10**18))
print("Publisher account Ocean balance: {:>6.1f}".format(ocn.accounts.balance(publisher_acct).ocn/10**18))

""" 
3) Prepare metadata
"""

# Example of response after storing the dataset in a distributed file system
response = {'IpfsHash': 'QmdgRMZzczorCywKqKZfKnvbzR9KgDgJuZJ3fw1z95YsRZ',
            'PinSize': 10615,
            'Timestamp': '2020-06-05T10:54:12.474Z'}

# Using response to update/create the metadata
metadata = generate_metadata_dict(response)

# Example of URL where dataset is stored and that would be added to metadata
response = "https://www.gov.uk/guidance/the-r-number-in-the-uk"

# Append to previous metadata
metadata = generate_metadata_dict(response, metadata)

""" 
4) Publish the asset into Ocean Protocol
"""
ddo = ocn.assets.create(metadata, publisher_acct)
registered_did = ddo.did
print("New asset registered at", registered_did)

ddo_dict = ddo.as_dictionary()
print("DID:", ddo.did)
print("Services within this DDO:")
for svc in ddo_dict['service']:
    print(svc['type'], svc['serviceEndpoint'])

for file_attrib in ddo.metadata['main']['files']:
    assert 'url' not in file_attrib
print("Encrypted files decrypt on purchase! Cipher text: [{}...] . ".format(ddo.metadata['encryptedFiles'][:50]))

""" 
5) Verify that the asset exists in the MetaData storage
"""
print("Wait for the transaction to complete!")
sleep(10)
web3 = Web3Provider.get_web3()
event = ocn.keeper.did_registry.subscribe_to_event(
    ocn.keeper.did_registry.DID_REGISTRY_EVENT_NAME,
    30,
    {'_did': web3.toBytes(hexstr=ddo.asset_id)},
    from_block=0,
    wait=True
)

ddo = ocn.assets.resolve(registered_did)
print("Asset '{}' resolved from Aquarius metadata storage: {}".format(ddo.did, ddo.metadata['main']['name']))

# We need the pure ID string as in the DID registry (a DID without the prefixes)
asset_id = did_to_id(registered_did)
owner = ocn.keeper.did_registry.contract_concise.getDIDOwner(asset_id)
print("Asset ID", asset_id, "owned by", owner)
assert str.lower(owner) == str.lower(publisher_acct.address)
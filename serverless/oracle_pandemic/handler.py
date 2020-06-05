import json

from covid_data_sources import get_coronavirus_data_gov_uk
from covid_data_sources import get_r_rate
from covid_data_sources import get_business_types_regulated
from ipfs.IPFShandler   import pin_json_to_ipfs

"""
TODO notes
trigger store of content
use queue
subscribe to results
when results are available then assemble and return
caching needs to be considered
if modified since & etag
hash of all data, source and derived computed
store this until the underlying data changes
give a request id that can be queried later
may need mapping between request and hashed state
need to store state, use day as timestamp and pull from ipfs?s3/db
hash of refs to hashes
wait for responses first

"""

def check_pandemic(event, context):
    body = is_pandemic_in_force(event)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def check_corona_cases_uk(event, context):
    body = get_corona_cases_uk(event, context)
    reference = pin_json_to_ipfs(body)
    print(reference)
    if reference is not None:
        ipfs_data = json.loads(reference)
        print(ipfs_data)
        ipfs_data_body = json.loads(ipfs_data["body"])
        print(ipfs_data_body)
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def get_uk_alert_level(event, context):
    # check for regional specific queries
    level = {"current_level": 4}

    response = {
        "statusCode": 200,
        "body": json.dumps(level)
    }

    return response

def get_uk_infection_rate_level(event, context):
    # check for regional specific queries
    body = get_corona_infection_rate_uk(event, context)
    # body = {"error": "coronadata content changed"}

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


# Oracle records that there is a pandemic in [England]
def is_pandemic_in_force(query_attributes, *args, **kwargs):
    # check query_attributes for nation specifics (e.g. Scotland and NI may have different restrictions and status)

    structured_text = {
        "event_type": "pandemic",
        "event_name": "COVID-19",
        "event_designation_date": "2020-03-11T00:16:26-00:00", # WHO press release and twitter 4:26 PM GMT
        "event_category": "https://www.wikidata.org/wiki/Q81068910", # schema.org defined event for covid-19 related events

        "resulting_action": "action_by_government",
        "resulting_action_source": "government_UK",
        "action_type": "business_closure",
        "date_of_closure": "2020-03-23T00:00:00-00:00",
        "regions_affected": ["England"],
        # "business_type": ["hairdressers", "barbers", "beauty and nail salons, including piercing and tattoo parlours'"]
    }
    # structured_text["business_type"] = get_business_types_regulated.get_content(*args, **kwargs)
    structured_text["business_type"] = business_closures
    return structured_text


def get_corona_cases_uk(event, context, *args, **kwargs):
    return get_coronavirus_data_gov_uk.get_content(*args, **kwargs)


def get_corona_infection_rate_uk(event, context, *args, **kwargs):
    return get_r_rate.get_content(*args, **kwargs)

business_closures = {
    "business_closures": [
        "Workplace canteens may remain open where there is no practical alternative for staff at that workplace to obtain food",
        "Public houses",
        "Cinemas",
        "Theatres",
        "Nightclubs",
        "Bingo halls",
        "Concert halls",
        "Museums and galleries",
        "Casinos",
        "Betting shops",
        "Spas",
        "Massage parlours",
        "Tattoo and piercing parlours",
        "Skating rinks",
        "Funfairs (whether outdoors or indoors)",
        "Outdoor markets",
        "Car showrooms",
        "Auction houses",
        "Restaurants",
        "Restaurants and dining rooms in hotels or members' clubs",
        "Bars",
        "Bars in hotels or members' clubs",
        "Nail",
        "Beauty",
        "Hair salons and barbers",
        "Indoor fitness studios",
        "Gyms",
        "Swimming pools",
        "Bowling alleys",
        "Amusement arcades or soft play areas or other indoor leisure centres or facilities",
        "Playgrounds",
        "Sports courts",
        "Cafes",
        "Workplace canteens"
    ],
    "business_exceptions": [
        "Off licenses and licensed shops selling alcohol ( breweries)",
        "Pharmacies ( non-dispensing pharmacies) and chemists",
        "Newsagents",
        "Petrol stations",
        "Car repair and mot services",
        "Bicycle shops",
        "Short term loan providers",
        "Post offices",
        "Funeral directors",
        "Laundrettes and dry cleaners",
        "Veterinary surgeons and pet shops",
        "Agricultural supplies shop",
        "Car parks",
        "Public toilets",
        "Garden centres",
        "Outdoor sports courts",
        "Food retailers",
        "Food markets",
        "Supermarkets",
        "Convenience stores and corner shops",
        "Homeware",
        "Building supplies and hardware stores",
        "Banks",
        "Credit unions",
        "Savings clubs",
        "Undertakings which by way of business operate currency exchange offices",
        "Dental services",
        "Opticians",
        "Audiology services",
        "Chiropody",
        "Chiropractors",
        "Services relating to mental health",
        "Storage and distribution facilities",
        "Where the facilities are in the premises of a business included in this part",
        "Building societies",
        "Cash points",
        "Taxi",
        "Vehicle hire businesses",
        "Transmit money (or any representation of money) by any means",
        "Cash cheques which are made payable to customers",
        "Osteopaths and other medical",
        "Health services",
        "Delivery drop off",
        "Collection points"
    ]
}
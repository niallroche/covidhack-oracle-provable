import json

def check_pandemic(event, context):
    body = is_pandemic_in_force(event)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def check_corona_cases_uk(event, context):
    body = get_corona_cases_uk(event, context)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def get_uk_alert_level(event, context):
    # check for regional specific queries
    level = {"current_level": 3}

    response = {
        "statusCode": 200,
        "body": json.dumps(level)
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
def is_pandemic_in_force(query_attributes):
    # check query_attributes for nation specifics (e.g. Scotland and NI may have different restrictions and status)

    structured_text = {
        "force_majeure": True,
        "event_type": "pandemic",
        "event_name": "COVID-19",
        "event_designation_date": "2020-03-11T00:16:26-00:00", # WHO press release and twitter 4:26 PM GMT
        "event_category": "https://www.wikidata.org/wiki/Q81068910", # schema.org defined event for covid-19 related events

        "resulting_action": "action_by_government",
        "resulting_action_source": "government_UK",
        "action_type": "business_closure",
        "date_of_closure": "2020-03-23T00:00:00-00:00",
        # "business_type": ["hairdressers", "barbers", "beauty and nail salons, including piercing and tattoo parlours'"]
      }
    return structured_text

def get_corona_cases_uk(event, context, *args, **kwargs):
    corona_cases_uk = {
        "Total number of lab-confirmed UK cases": 246406,
        "Daily number of lab-confirmed UK cases": 2684,
        "Total number of COVID-19 associated UK deaths": 34796,
        "Daily number of COVID-19 associated UK deaths": 160,

        "nations": [
            {"nation": "England", "total_cases": 144127, "rate": 257.5, "total_deaths": 31010},
            {"nation": "Northern Ireland", "total_cases": 4401, "rate": 233.9, "total_deaths": 476},
            {"nation": "Scotland", "total_cases": 14594, "rate": 268.4, "total_deaths": 2103},
            {"nation": "Wales", "total_cases": 12404, "rate": 395.2, "total_deaths": 1207}
        ],

        "regions": [],

        "UTLA": [{"region": "Worcestershire", "total_cases": 1334, "rate": 225.3}],

        "LTLA": [{"region": "Malvern Hills", "total_cases": 137, "rate": 175.4}]
    }
    return corona_cases_uk

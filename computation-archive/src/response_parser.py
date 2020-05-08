import json


"""
Length of closure
We are asking the businesses and venues outlined above not to open for trade from close of trade 23 March 2020.
"""

response = {
    'closure_periods': [
        {'date_of_closure': '23 March 2020',
         'affected_sectors': [
             {'sector_type': 'Food and drink',
                'business_types': [
                    {'business_type': 'Restaurants and public houses, wine bars or other food and drink establishments including within hotels and members’ clubs',
                    'exceptions': 'Food delivery and takeaway can remain operational and can be a new activity supported by the new permitted development right. This covers the provision of hot or cold food that has been prepared for consumers for collection or delivery to be consumed, reheated or cooked by consumers off the premises.'},
                    {'business_type': 'Cafés and canteens',
                     'exceptions': 'Food delivery and takeaway can remain operational (and as above). Cafés and canteens at hospitals, police and fire services’ places of work, care homes or schools; prison and military canteens; services providing food or drink to the homeless. Where there are no practical alternatives, other workplace canteens can remain open to provide food for their staff and/or provide a space for breaks. However, where possible, staff should be encouraged to bring their own food, and distributors should move to takeaway. Measures should be taken to minimise the number of people in the canteen / break space at any one given time, for example by using a rota.'}
                ]}
        ]}
    ]}
"""

             {'sector_type': 'Retail',
                'business_types': [
                    {'business_type': 'Hairdressers, barbers, beauty and nail salons, including piercing and tattoo parlours',
                     'Exceptions': ''},
                    {'business_type': 'All retail with notable exceptions',
                     'Exceptions': ' Supermarkets and other food shops

• Medical services (such as dental surgeries, opticians and audiology clinics, physiotherapy clinics, chirpody and podiatry clinics, and other professional vocational medical services)

• Pharmacies and chemists, including non-dispensing pharmacies

• Petrol stations

• Bicycle shops

• Hardware shops and equipment, plant and tool hire

• Veterinary surgeries and pet shops

• Agricultural supplies shops

• Corner shops and newsagents

• Off-licences and licenced shops selling alcohol, including those within breweries

• Laundrettes and dry cleaners

• Post offices

• Vehicle rental services

• Car garages and MOT services

• Car parks

• High street banks, building societies, short-term loan providers, credit unions and cash points

• Storage and distribution facilities, including delivery drop off points where they are on the premises of any of the above businesses

• Public toilets

• Shopping centres may stay open but only units of the types listed above may trade'},
         ]
         }]
}



"""

def parse_response(res, **kwargs):
    parsed_text = res.text
    # TODO add parsing logic here

    # starting with a basic timestamp to set the closed date
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
    test = "test"

    schema_codid_announcement = {
        "@context": "http://schema.org",
        "@type": "SpecialAnnouncement",
        "name": "Stanford announce COVID-19 testing facility",
        "text": "",
        "datePosted": "2020-03-16",
        "url": "http://med.stanford.edu/news/all-news/2020/03/stanford-offers-drive-through-coronavirus-test.html",
        "category": "https://www.wikidata.org/wiki/Q81068910",
        "about" : {
           "@type": "CovidTestingFacility",
           "name": "Stanford Health Care",
           "url": "https://stanfordhealthcare.org/"
        }
    }

    schema_school_closure = {
        "@context": "http://schema.org",
        "@type": "SpecialAnnouncement",
        "name": "School Closure information for Eastergate School",
        "text": "School closure information has been published.",
        "datePosted": "2020-03-17",
        "expires": "2020-03-24",
        "category": "https://www.wikidata.org/wiki/Q81068910",
        "schoolClosuresInfo": "http://example.org/schools/school/eastergate-cofe-primary-school/closures",
        "webFeed": {
          "@type": "DateFeed",
          "@url": "http://example.org/schools/school/eastergate-cofe-primary-school/closures",
          "encodingFormat": "application/rss+atom"
        },
        "about" : {
            "@type": "School",
            "name": "Eastergate School",
            "url": "http://example.org/schools/school/eastergate-cofe-primary-school/",
            "location": "..."
        }
    }

    schema_business_closure = {
        "@context": "http://schema.org",
        "@type": "SpecialAnnouncement",
        "name": "Closing certain businesses and venues",
        "text": "Closing certain businesses and venues",
        "datePosted": "2020-04-24", #this is the date updated, not first posted
        # "expires": "2020-03-24",
        "category": "https://www.wikidata.org/wiki/Q81068910",
        "businessClosuresInfo": "https://www.gov.uk/government/publications/further-businesses-and-premises-to-close/further-businesses-and-premises-to-close-guidance", # adapted from school closure

        "announcementLocation": "uk", # CivicStructure geoCovers place
        # "category:" "SpecialAnnouncement",

        "webFeed": {
          "@type": "DateFeed",
          "@url": "https://www.gov.uk/government/publications/further-businesses-and-premises-to-close/further-businesses-and-premises-to-close-guidance",
          "encodingFormat": "text/html"
        }
        # could list types of local business affected
    }

    parsed_text = json.dumps(structured_text)
    # parsed_text = '{}'

    return parsed_text
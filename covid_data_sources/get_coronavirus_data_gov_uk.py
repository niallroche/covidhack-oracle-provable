# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2020 Walter Hernandez

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
"""

import requests as requests
from datetime import datetime
import json

def get_content(*args, **kwargs):

    # Takes the JSON files that are used to transfer the information to generate the dashboards in coronavirus.data.gov.uk
    # This allows to get the information in real time
    lates_cases = requests.get('https://c19downloads.azureedge.net/downloads/data/landing.json').json()
    population = requests.get('https://c19pub.azureedge.net/assets/population/population.json').json()
    nations = requests.get('https://c19downloads.azureedge.net/downloads/data/countries_latest.json').json()
    regions = requests.get('https://c19downloads.azureedge.net/downloads/data/regions_latest.json').json()
    utlas = requests.get('https://c19downloads.azureedge.net/downloads/data/utlas_latest.json').json()
    ltla = requests.get('https://c19downloads.azureedge.net/downloads/data/ltlas_latest.json').json()

    corona_cases_uk = {
            "Total number of lab-confirmed UK cases": lates_cases['overview']['K02000001']['totalCases']['value'],
            "Daily number of lab-confirmed UK cases": lates_cases['overview']['K02000001']['newCases']['value'],
            "Total number of COVID-19 associated UK deaths": lates_cases['overview']['K02000001']['deaths']['value'],
            "Daily number of COVID-19 associated UK deaths": lates_cases['overview']['K02000001']['latestDeaths']['value'],
        }

    nations_corrected = []
    format_date = "%Y-%m-%d"

    # The rate is calculated within the dashboard of coronavirus.data.gov.uk by dividing:
    # (Total cases for a region / population for a region) * 100000
    # This is calculation is replicated using the same information transferred for the calculation in the dashboard of coronavirus.data.gov.uk
    # The rest of the information is the same used in coronavirus.data.gov.uk
    for key, value in nations.items():

        if "name" in value.keys():

            nations_dict = {"nation": value['name']['value'],
                            "total_cases": value['totalCases']['value'],
                            "rate": round((value['totalCases']['value'] / population[key]) * 100000, 1),
                            "total_deaths": value['deaths']['value']}

            if "dailyConfirmedCases" in value.keys():

                # Gets the latest date of the information available
                latest_date_info = max([v['date'] for v in value['dailyConfirmedCases']])

                # Filters the latest dailyConfirmedCases for the latest month (30 days) counting backwards from the latest date of the information available
                last_month_cases = [v for v in value['dailyConfirmedCases'] if (datetime.strptime(latest_date_info, format_date) - datetime.strptime(v['date'], format_date)).days <= 30]

                nations_dict["total_cases_last_month"] = {"total_cases": sum([v['value'] for v in last_month_cases]),
                                                          "time_period_start": min([v['date'] for v in last_month_cases]),
                                                          "time_period_end": max([v['date'] for v in last_month_cases])}

            if 'dailyDeaths' in value.keys():

                # Gets the latest date of the information available
                latest_date_info = max([v['date'] for v in value['dailyDeaths']])

                # Filters the latest dailyDeaths for the latest month (30 days) counting backwards from the latest date of the information available
                last_month_deaths = [v for v in value['dailyDeaths'] if (datetime.strptime(latest_date_info, format_date) - datetime.strptime(v['date'], format_date)).days <= 30]

                nations_dict["total_deaths_last_month"] = {"total_cases": sum([v['value'] for v in last_month_deaths]),
                                                          "time_period_start": min([v['date'] for v in last_month_deaths]),
                                                          "time_period_end": max([v['date'] for v in last_month_deaths])}

            nations_corrected.append(nations_dict)

    regions_corrected = []
    for key, value in regions.items():

        if key in population.keys():

            region_dict = {"region": value['name']['value'],
                           "total_cases": value['totalCases']['value'],
                           "rate": round((value['totalCases']['value'] / population[key]) * 100000, 1)}

        if region_dict not in regions_corrected:
            regions_corrected.append(region_dict)

    utlas_corrected = []
    for key, value in utlas.items():

        if key in population.keys():

            utlas_dict = {"region": value['name']['value'],
                           "total_cases": value['totalCases']['value'],
                           "rate": round((value['totalCases']['value'] / population[key]) * 100000, 1)}

        if utlas_dict not in utlas_corrected:
            utlas_corrected.append(utlas_dict)

    ltla_corrected = []
    for key, value in ltla.items():

        if key in population.keys():

            ltla_dict = {"region": value['name']['value'],
                           "total_cases": value['totalCases']['value'],
                           "rate": round((value['totalCases']['value'] / population[key]) * 100000, 1)}

        if ltla_dict not in ltla_corrected:
            ltla_corrected.append(ltla_dict)

    for name, dict_values in zip(['nations', 'region', 'UTLA', 'LTLA'], [nations_corrected, regions_corrected, utlas_corrected, regions_corrected]):
        corona_cases_uk[name] = dict_values

# with open('corona_cases_uk.json', 'w+') as json_file:
#     json.dump(corona_cases_uk, json_file, indent=4)
#
# json_data = json.dumps(corona_cases_uk, indent=4)
# print(json_data)

    return corona_cases_uk
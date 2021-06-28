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

import requests
from datetime import datetime
import json


def get_content(*args, **kwargs):
    """
    :param args:
    :param kwargs:
    :return: dictionary with "overview", "nation", "region", "utla", "ltla" as sub-dictionaries
            with values for each: total_cases, rate, and total_deaths
    """

    # Using https://coronavirus.data.gov.uk api
    ENDPOINT = "https://api.coronavirus.data.gov.uk/v1/data"
    AREA_TYPES = ["overview", "nation", "region", "utla", "ltla"]
    # AREA_NAMES = ["england", "scotland", "northern ireland", "wales"]

    format_date = "%Y-%m-%d"
    date = datetime.now().strftime(format_date)

    corona_cases_uk = {}
    for areaType in AREA_TYPES:

        filters = [
            f"areaType={areaType}",
            # f"date={date}"
            # f"areaName={areaName}"
        ]

        if areaType == "nation":
            dailyCases = "newCasesByPublishDate"
            cumulativeCases = "cumCasesByPublishDate"
            cumulativeCasesRate = "cumCasesByPublishDateRate"
            latestBy = "newCasesByPublishDate"
        else:
            dailyCases = "newCasesBySpecimenDate"
            cumulativeCases = "cumCasesBySpecimenDate"
            cumulativeCasesRate = "cumCasesBySpecimenDateRate"
            latestBy = "newCasesBySpecimenDate"

        structure = {
            "date": "date",
            "name": "areaName",
            "code": "areaCode",
            "dailyCases": f"{dailyCases}",
            "cumulativeCases": f"{cumulativeCases}",
            "cumulativeCasesRate": f"{cumulativeCasesRate}",
            "dailyDeaths": "newDeaths28DaysByPublishDate",
            "cumulativeDeaths": "cumDeaths28DaysByPublishDate",
            "cumulativeDeathsRate": "cumDeaths28DaysByDeathDateRate"

            ###########
            # Total number of deaths since the start of the pandemic of people whose death certificate mentioned
            # COVID-19 as one of the causes. The data are published weekly by the ONS, NRS and NISRA and there is
            # a lag in reporting of at least 11 days because the data are based on death registrations
            ############
            # "dailyDeaths": "newDailyNsoDeathsByDeathDate",
            # "cumulativeDeaths": "cumOnsDeathsByRegistrationDate",
            # "cumulativeDeathsRate":"cumOnsDeathsByRegistrationDateRate"
        }

        api_params = {
            "filters": str.join(";", filters),
            "structure": json.dumps(structure, separators=(",", ":")),
            "latestBy": latestBy
        }

        response = requests.get(ENDPOINT, params=api_params, timeout=10)
        response = response.json()['data']

        if areaType == "overview":
            response = response[0]
            corona_cases_uk = {
                "date": response['date'],
                "total_cases": response['cumulativeCases'],
                "daily_cases": response['dailyCases'],
                "rate": response['cumulativeCasesRate'],
                "total_deaths": response['cumulativeDeaths'],
                "daily_deaths": response['dailyDeaths']
            }

        else:
            dict_values = []

            for r in response:

                filters = [
                    f"areaType={areaType}",
                    # f"date={r['date']}",
                    f"areaName={r['name']}"
                ]

                # Do another request to get the data with all the dates for an area
                api_params = {
                    "filters": str.join(";", filters),
                    "structure": json.dumps(structure, separators=(",", ":")),
                }

                # Get data specific for an area to filter the data for latest month
                r_area = requests.get(ENDPOINT, params=api_params, timeout=10)
                r_area = r_area.json()['data']

                ## Get the data for a month range
                # Period end is the date of the latest value added
                time_period_end = r_area[0]['date']
                last_month_cases_deaths = [v for v in r_area if (
                                datetime.strptime(time_period_end, format_date) - datetime.strptime(v['date'],
                                                                                                     format_date)).days <= 30]
                time_period_start = min([v['date'] for v in last_month_cases_deaths])

                dict_values.append({
                    areaType: r["name"],
                    "date": r['date'],
                    "total_cases": r['cumulativeCases'],
                    "daily_cases": r['dailyCases'],
                    "rate": r['cumulativeCasesRate'],
                    "total_deaths": r['cumulativeDeaths'],
                    "daily_deaths": r['dailyDeaths'],
                    "total_cases_last_month":{
                        "total_cases": sum([v['dailyCases'] for v in last_month_cases_deaths if v['dailyCases'] is not None]),
                                        "time_period_start": time_period_start,
                                        "time_period_end": time_period_end},
                    "total_deaths_last_month": {
                                        "total_deaths": sum([v['dailyDeaths'] for v in last_month_cases_deaths if v['dailyDeaths'] is not None]),
                                        "time_period_start": time_period_start,
                                        "time_period_end": time_period_end}
                })

            # Add all the values scraped
            corona_cases_uk[areaType] = dict_values

    return corona_cases_uk

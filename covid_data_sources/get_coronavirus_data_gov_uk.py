import requests as requests

def get_content(*args, **kwargs):

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
    for key, value in lates_cases['countries'].items():

        nations_dict = {"nation": value['name']['value'],
                       "total_cases": value['totalCases']['value'],
                       "rate": round((value['totalCases']['value'] / population[key]) * 100000, 1),
                       "total_deaths": value['deaths']['value']}

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

    return corona_cases_uk
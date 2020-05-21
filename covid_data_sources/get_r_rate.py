import requests as requests
from lxml import html
import re
import json

def get_content(*args, **kwargs):

    r_rate_data = {}
    response = requests.get('https://epiforecasts.io/covid/posts/national/united-kingdom/')

    tree = html.fromstring(response.content)
    table_content = tree.xpath('//div[@data-layout="l-body-outset"]/table//tr')

    regions = []
    for value in table_content:
        value = value.xpath('.//td//text()')

        if len(value) != 0:
            r_rate = [float(s) for s in re.findall(r'[+-]?(\d+(?:\.\d+)?)',value[3].strip())]
            regions_dict = {"region": value[0].strip(),
                            "effective_reproductive_number_(r_rate)": {"r_rate": r_rate[0],
                                                                       "lower_bound": r_rate[1],
                                                                       "upper_bound": r_rate[2]}
                            }

            regions.append(regions_dict)

    r_rate_data['regions'] = regions

    # with open('r_rate_data.json', 'w+') as json_file:
    #     json.dump(r_rate_data, json_file, indent=4)

    return r_rate_data







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







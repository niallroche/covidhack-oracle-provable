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

__author__ = "Walter Hernandez"
__copyright__ = "Copyright 2021"
__credits__ = ["Niall Roche"]
__license__ = "MIT License"
__version__ = "1.0"

import re
import requests


def get_content(*args, **kwargs):
    r_rate_data = {}

    # Get api data used to feed tables for each country
    response = requests.get('https://epiforecasts.io/covid/posts/posts.json')
    if response.status_code == 200:
        response = response.json()
    else:
        raise Exception("No access to API data")

    # Filter the desired regions
    response = [d for d in response if
                "united kingdom" in [c.lower() for c in d['categories']] and "subnational" in d[
                    'path'] and "local" not in d['path']]

    regions = []
    for region in response:
        r_rate = [c.lower() for c in region['contents'].splitlines()]

        r_rate_index = [i for i, v in enumerate(r_rate) if
                        any(s in v for s in ['effective reproduction no', "rate of growth"])]

        r_rate = "\n".join(r_rate[r_rate_index[0]:r_rate_index[1]])
        r_rate = [float(s) for s in re.findall(r'[+-]?(\d+(?:\.\d+)?)', r_rate.strip())]

        regions_dict = {"region": region['title'].replace("Estimates for", "").replace("(United Kingdom)", "").strip(),
                        "effective_reproductive_number_(r_rate)": {"r_rate": r_rate[0],
                                                                   "lower_bound": r_rate[1],
                                                                   "upper_bound": r_rate[2]}
                        }

        regions.append(regions_dict)

    r_rate_data['regions'] = regions

    return r_rate_data

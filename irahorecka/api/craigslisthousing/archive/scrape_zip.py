"""
/irahorecka/api/craigslisthousing/archive/scrape_zip.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scrapes every zipcode for these counties:
santa clara
santa cruz
san mateo
san francisco
alameda
contra costa
napa
marin
sonoma


Export as JSON file as a large dictionary with zipcode keys. Children dict with lat/lon keys:
{"94901": {"lat": "37.972423", "lon": "-122.51484"}, "94903": {"lat": "38.019022", "lon": "-122.54589"}, ... }
"""

import json
from pathlib import Path

import requests
import pandas as pd
from bs4 import BeautifulSoup

MODULE_PATH = Path(__file__).absolute().parent

COUNTY_URL = {
    "marin": "http://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?ClientCode=capitolimpact&State=ca&StName=California&StFIPS=06&FIPS=06041",
    "san_mateo": "http://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?ClientCode=capitolimpact&State=ca&StName=California&StFIPS=06&FIPS=06081",
    "san_francisco": "http://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?ClientCode=capitolimpact&State=ca&StName=California&StFIPS=06&FIPS=06075",
    "alameda": "http://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?ClientCode=capitolimpact&State=ca&StName=California&StFIPS=06&FIPS=06001",
    "contra_costa": "http://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?ClientCode=capitolimpact&State=ca&StName=California&StFIPS=06&FIPS=06013",
    "solano": "http://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?ClientCode=capitolimpact&State=ca&StName=California&StFIPS=06&FIPS=06095",
    "napa": "http://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?ClientCode=capitolimpact&State=ca&StName=California&StFIPS=06&FIPS=06055",
    "sonoma": "http://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?ClientCode=capitolimpact&State=ca&StName=California&StFIPS=06&FIPS=06097",
    "santa_clara": "http://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?ClientCode=capitolimpact&State=ca&StName=California&StFIPS=06&FIPS=06085",
    "santa_cruz": "http://www.ciclt.net/sn/clt/capitolimpact/gw_countydet.aspx?ClientCode=capitolimpact&state=ca&stfips=06&stname=California&fips=06087",
}


def get_zip(html):
    zipcodes = html.find("table")
    zip_county = [zipcode.text for zipcode in zipcodes.find_all("a")]
    # Kinda crappy way to achieve this below... any better?
    tupled_zip_county = []
    tuple_array = []
    for idx, item in enumerate(zip_county):
        tuple_array.append(item)
        if (idx + 1) % 3 == 0:
            tupled_zip_county.append(tuple_array)
            tuple_array = []

    # return list(map(lambda x: {x[1]: x[0]}, tupled_zip_county))
    return list(map(lambda x: x[0], tupled_zip_county))


def get_html(url):
    content = requests.get(url).text
    return BeautifulSoup(content, "lxml")


def zip_lat_lon(zipcode):
    zip_df = pd.read_csv(MODULE_PATH.joinpath("zipcode.csv"))[["zip", "latitude", "longitude"]]
    caller_zip = zip_df.loc[zip_df["zip"] == int(zipcode)]
    return tuple(map(lambda x: str(caller_zip.iloc[0][x]), ["zip", "latitude", "longitude"]))


def write_json(data, output_path):
    """Writes dictionary to JSON file."""
    with open(output_path, "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    # Scrapes zipcodes within the bay area from the web, writes json file mapping zipcodes to their lat/lon coord
    zips_nested = [get_zip(get_html(COUNTY_URL[county])) for county in COUNTY_URL]
    zips = [zipcode for sub_zip in zips_nested for zipcode in sub_zip if zipcode.isdigit()]
    zips_dict = {
        zip_tup[0].strip(".0"): {"lat": zip_tup[1], "lon": zip_tup[2]}
        for zip_tup in [zip_lat_lon(zipcode) for zipcode in zips]
    }
    write_json(zips_dict, "sfbay_zipcodes.json")

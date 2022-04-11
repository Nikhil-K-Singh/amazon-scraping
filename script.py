#!/usr/bin/env python3
from helper import level_1, level_2, level_3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from lxml import etree

import json, pprint, ssl, sys, re, os

import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def main(url, ASIN):
    df = pd.DataFrame(
        columns=[
            "ASIN",
            "Average Rating",
            "Global Rating Count",
            "5 stars percent",
            "4 stars percent",
            "1 star percent",
            "Reviews",
        ]
    )
    print(f"going with url=> {url}")
    # We need to bypass the SSL certificate errors
    # mimic identity as web browser for the website
    req = Request(
        url,
        data=None,
        headers={"User-Agent": "Mozilla/5.0"},
        origin_req_host=None,
        unverifiable=False,
        method=None,
    )
    page = urlopen(req).read()

    # Generate a Soup object of the webpage for extracting data
    soup = BeautifulSoup(page, "html.parser")

    Star_Rating = level_1(soup)
    soup_for_3, Reviews_Count, Summary_5Star, Summary_4Star, Summary_1Star = level_2(
        soup
    )

    # the reviews are extracted from a new page which we had already traversed in level_2, thus we reuse the soup
    Reviews = level_3(soup_for_3)

    to_append = [
        ASIN,
        Star_Rating,
        Reviews_Count,
        Summary_5Star,
        Summary_4Star,
        Summary_1Star,
        Reviews,
    ]
    a_series = pd.Series(to_append, index=df.columns)
    df = df.append(a_series, ignore_index=True)
    df.to_csv("Result.csv", mode="a", index=False, header=False)


if __name__ == "__main__":
    # check if the Result.csv already exists
    if os.path.isfile("./Result.csv"):
        pass
    else:
        df = pd.DataFrame(
            columns=[
                "ASIN",
                "Average Rating",
                "Global Rating Count",
                "5 stars percent",
                "4 stars percent",
                "1 star percent",
                "Reviews",
            ]
        )
        df.to_csv("Result.csv", index=False)

    # Taking the URL as input from the user
    ASIN = ""
    ASINS = input(
        """
    Paste the comma seperated Amazon ASINs for the Products,
    leave blank to go with default product\n"""
    )

    if ASINS == "":
        ASIN = "B007A4SDCG"
        url = f"""https://www.amazon.in/s?k={ASIN}"""
        main(url, ASIN)
    else:
        ASINS = ASINS.split(",")
        for ASIN in ASINS:
            url = f"""https://www.amazon.in/s?k={ASIN}"""
            main(url, ASIN)

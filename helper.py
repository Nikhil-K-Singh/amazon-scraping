from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from lxml import etree

def level_1(soup, css_select="a-icon-alt"):
    """
    Level 1: Extract “4.2 out of 5” for a list of products/ASINs.
    """
    # Extracting the rating element via the CSS attribute
    Level_1_extraction = soup.select(f".{css_select}")

    # get the data of the resultset and clip only for the value we need
    return str(Level_1_extraction[0].text)


def level_2(soup):
    """
    Level 2: (above level +) Extract “472 global ratings” and percentage distribution of 5 star, 4 star, 1 star ratings.
    """
    Level_2_extraction = soup.select("div > h2 > a")
    # create a fresh new url for specific data
    new_url = "https://www.amazon.in" + Level_2_extraction[0]["href"]
    # print("New Page URL:\t",new_url)

    req = Request(
        new_url,
        data=None,
        headers={"User-Agent": "Mozilla/5.0"},
        origin_req_host=None,
        unverifiable=False,
        method=None,
    )
    page = urlopen(req).read()

    # Generate a Soup object of the webpage for extracting data
    soup = BeautifulSoup(page, "html.parser")

    # Extract the global ratings count data
    Customer_Reviews = soup.select('div[data-hook="total-review-count"] > span')
    Customer_Reviews_Count = Customer_Reviews[0].getText().strip().split()[0]

    rating_summary = soup.select('span[class="a-size-base"] > a')
    rating_summary_list = []
    for i in [0, 2, -1]:
        rating_summary_list.append(str(rating_summary[i]["title"]))

    return soup,Customer_Reviews_Count, rating_summary_list[0],rating_summary_list[1],rating_summary_list[2]


def level_3(soup):
    """
    Level 3: (above level +) Extract individual reviews given for the product.
    """
    all_review = soup.select('a[data-hook="see-all-reviews-link-foot"]')
    all_review_link = "https://www.amazon.in/" + all_review[0]["href"]

    req = Request(
        all_review_link,
        data=None,
        headers={"User-Agent": "Mozilla/5.0"},
        origin_req_host=None,
        unverifiable=False,
        method=None,
    )
    page = urlopen(req).read()

    # Generate a Soup object of the webpage for extracting data
    soup = BeautifulSoup(page, "html.parser")
    reviews = []
    for i in soup.findAll("span", {"data-hook": "review-body"}):
        reviews.append(i.text)
    review_summary=str(reviews)
    return review_summary
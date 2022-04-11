# amazon-scraping

The objective here is to build a scraper/crawler to extract customer ratings and reviews of products on Amazon


> Task 1: Extract “4.2 out of 5” for a list of products/ASINs.

> Task 2: Extract “472 global ratings” and percentage distribution of 5 star, 4 star, ... 1 star ratings.

> Task 3: Extract individual reviews given for the product.

----------------------------------------------------------------------

The approach here is using requests library to fetch the webpage and beautifulsoup to parse the content.

Each task is implemented in a seperate function within the helper.py file

The script.py is the one where the user input is parsed to make appropriate request and GET the data

further functions are called upon with appropriate parameters to parse the relevant data.

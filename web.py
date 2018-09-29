# -*- coding: utf-8 -*-
from googlesearch import search
import urllib.request
from bs4 import BeautifulSoup


def get_info(name):
    url = "https://coinmarketcap.com/currencies/{}/historical-data/".format(name.replace(" ", "-"))
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
            try:
                url = next(search(name + " coinmarketcap", num=1, stop=1)) + "historical-data/"
            except:
                return "Wrong name, can't find it at all"

            if "coinmarketcap" not in url:
                return "The cryptocurrency is not found on CMC"

    except UnicodeEncodeError:
        return "The name of cryptocurrency must consist of the English letters"

    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, "lxml")

    return """{0}{1}\n${2}{3}{4}Cap. ${7}Vol. ${5}{6}""".format(*extract_info(soup))


def extract_info(soup):
    name = soup.find("h1", {'class': 'text-large'}).text.split()     # [0] - short name [1] - fullname

    quote = soup.find("span", id="quote_price").text.split()[0]

    change = soup.find("span", {'class': 'text-large2 negative_change'})

    market_cap = soup.find("div", {'class': "coin-summary-item-detail details-text-medium"}).span.find_all('span')[0]

    satoshiki = soup.find("span", {'class': "text-gray details-text-medium"}).text.replace("\n", " ")

    current_volume = soup.find_all("div", {'class': "coin-summary-item-detail details-text-medium"}
                                   )[1].find("span").text.split()[0].replace(",", "")  # getting volume in a very shitty way

    yesterday_params = soup.find("tr", {"class": "text-right"}).text.split()  # -2 - volume ; -1 - quote
    volume_rate = (-1 + float(current_volume) / float(yesterday_params[-2].replace(",", ""))) * 100

    if isinstance(change, type(None)):
        change = soup.find("span", {'class': 'text-large2 positive_change '})

    return name[1], name[0], quote, change.text[1:],\
        satoshiki, convert(current_volume), "({}%)".format(str(volume_rate)[:5]), convert(market_cap.text.replace(",",
                                                                                                                  ""))


def convert(number):
    number = float(number)
    length = len(str(int(number)))

    if 6 < length < 10:
        return str(round(number / 1000000, 2)) + "M"
    elif length > 9:
        return str(round(number / 1000000000, 3)) + "B"
    return str(round(number / 1000, 2)) + "K"


print(get_info("eth"))



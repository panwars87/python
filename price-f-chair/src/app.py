__author__ = "shashantp"

import requests
from bs4 import BeautifulSoup

# <span id="priceblock_ourprice" class="a-size-medium a-color-price">$49.99</span>

request = requests.get("https://www.amazon.com/gp/product/B00UI6F1AK/ref=s9_simh_gw_g21_i15_r?ie=UTF8&fpl=fresh&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=&pf_rd_r=S1WCG9XAJ1YT49J3TQKQ&pf_rd_t=36701&pf_rd_p=a6aaf593-1ba4-4f4e-bdcc-0febe090b8ed&pf_rd_i=desktop")
content = request.content
soup = BeautifulSoup(content, "html.parser")
element = soup.find("span", {"id": "priceblock_ourprice"})

print(element.text.strip())

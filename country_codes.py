# A scraper to create a pickle of the country codes for use in wunderScraper.py

from bs4 import BeautifulSoup
import requests
import pickle

page = "https://www.worldatlas.com/aatlas/ctycodes.htm"

r = requests.get(page)

soup = BeautifulSoup(r.text, "html.parser")

country_dict = {}
table = soup.find('table')
header_row = table.tbody.tr

first_header = header_row.td.text

country_rows = header_row.find_next_siblings()
# print(len(country_rows))
# run through the table and place each country name as the key and code as the value
for i in range(len(country_rows)):
    country = country_rows[i].td.text.lower()
    code = country_rows[i].td.find_next_sibling().text.lower()
    country_dict[country] = code
# print(country_dict)

with open("country_codes.pk", 'wb') as file:
    data = country_dict
    pickle.dump(data, file)

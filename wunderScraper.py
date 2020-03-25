#!/usr/bin/env python3

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pickle

city = input("Type in the city:(for United States of America add the two letter state "
             "code):\n> ")
city_data = city.split(' ')
if len(city_data[-1]) == 2:
    state = city_data.pop().lower()
    city = ('-').join(city_data).lower()
    city = state+'/'+city
else:
    city = ('-').join(city_data).lower()

country = input("Type in the country: \n> ")

country = country.lower()

with open('country_codes.pk', 'rb') as file:
    country_codes = pickle.load(file)
try:
    code = country_codes[country]
    # print(code)
except KeyError:
    print("Check the real name of the country as per: https://www.worldatlas.com/aatlas/ctycodes.htm ")
    quit()

city_url = "https://www.wunderground.com/weather/"+code+"/"+city
# print(city_url)


options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

try:
    driver.get(city_url)
    driver.implicitly_wait(30)
    settings_button = driver.find_element_by_xpath('/html/body/app-root/app-today/one-column-layout/wu-header/div/div/lib-settings/header/button/i')
    settings_button.click()
    driver.implicitly_wait(10)

    choose_celcius = driver.find_element_by_xpath('/html/body/app-root/app-today/one-column-layout/wu-header/div/div/lib-settings/header/div/div/a[2]').click()

    driver.implicitly_wait(30)

    site = driver.page_source
    # print("grabbed page")

    soup = BeautifulSoup(site, 'lxml')

    city_name = soup.find('h1').span.text
    print(city_name)
    forecast_block = soup.select("div.forecast-wrap.ng-star-inserted")   # gives a list

    for block in forecast_block:
        anchor = block.find('a', class_='hook')
        forecast = anchor.next_sibling.next_sibling.text
        day = block.find('span', class_='day').text
        print(f"{day}: {forecast}")
except AttributeError:
    print("Something went wrong while parsing the page, one of the tags does not have "
          "the required attribute")
finally:
    driver.quit()  # to close the browser entirely


#!/usr/bin/env python3

from bs4 import BeautifulSoup
import pickle

city = input("Type in the city:\n> ")
city = city.lower().replace(' ', '-')

country = input("Type in the country: \n> ")

country = country.lower()

with open('country_codes.pk', 'rb') as file:
    country_codes = pickle.load(file)

code = country_codes[country]

city_url = "https://www.wunderground.com/weather/"+code+"/"+city


from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
driver.get(city_url)

driver.implicitly_wait(30)
settings_button = driver.find_element_by_xpath('/html/body/app-root/app-today/one-column-layout/wu-header/div/div/lib-settings/header/button/i')
settings_button.click()
# print('settings selected')
driver.implicitly_wait(10)

choose_celcius = driver.find_element_by_xpath('/html/body/app-root/app-today/one-column-layout/wu-header/div/div/lib-settings/header/div/div/a[2]').click()

# print('celsius selected')
driver.implicitly_wait(30)

site = driver.page_source
# print("grabbed page")

soup = BeautifulSoup(site, 'lxml')
city_name = soup.find('h1').span.text
print(city_name)
forecast_block = soup.find('div', class_='forecast-wrap')
forecast_blocks = [forecast_block, forecast_block.next_sibling,
           forecast_block.next_sibling.next_sibling]
for block in forecast_blocks:
    anchor = block.find('a', class_='hook')
    forecast = anchor.next_sibling.next_sibling.text
    day = block.find('span', class_='day').text
    print(f"{day}: {forecast}")

driver.quit()  # to close the browser entirely


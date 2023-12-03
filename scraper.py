import pdb
import re

import requests
from bs4 import BeautifulSoup
from helper_constants import *
from helper_functions import *

def extract_recipe_details(url):

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error retrieving page: Status code {response.status_code}")
        return False

    # pdb.set_trace()
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all the ingredients
    ingredients_list_items = soup.find_all("li", class_="mntl-structured-ingredients__list-item")

    # extract numbers and materials
    ingredients = []
    quantity_pattern = re.compile('|'.join(unicode_fractions.keys()), re.IGNORECASE)
    for item in ingredients_list_items:
        quantity = item.find("span", {"data-ingredient-quantity": "true"}).get_text(strip=True)
        if quantity_pattern.search(quantity):
            frac = quantity_pattern.search(quantity).group(0)
            if len(quantity) == 3:
                whole = float(quantity[0])
                dec = unicode_fractions[frac]
                quantity = whole + dec
            elif len(quantity) == 1:
                quantity = unicode_fractions[frac]
        unit = item.find("span", {"data-ingredient-unit": "true"}).get_text(strip=True)
        name = item.find("span", {"data-ingredient-name": "true"}).get_text(strip=True)
        ingredients.append(f"{quantity} {unit} {name}".strip())

    # instruction steps
    steps = []

    ol = soup.find('ol', class_="comp mntl-sc-block-group--OL mntl-sc-block mntl-sc-block-startgroup")
    steps_items = ol.find_all('p',  class_="comp mntl-sc-block mntl-sc-block-html")
    for item in steps_items:
        steps.append(item.get_text(strip=True))

    # save ingredients and steps
    with open("data/steps.txt", "w", encoding='utf-8') as file:
        for step in steps:
            file.write(f"{step}\n")
    with open("data/ingredients.txt", "w", encoding='utf-8') as file:
        for ingredient in ingredients:
            file.write(f"{ingredient}\n")

    return True

# if __name__ == '__main__':
#     extract_recipe_details("https://www.allrecipes.com/miso-noodle-soup-in-a-jar-recipe-8350566")
#     get_tools("data/steps.txt")

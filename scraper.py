import pdb
import re

import requests
from bs4 import BeautifulSoup

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
    for item in ingredients_list_items:
        quantity = item.find("span", {"data-ingredient-quantity": "true"}).get_text(strip=True)
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


def get_tools():
    kitchen_tools = []
    with open("data/steps.txt", 'r', encoding='utf-8') as file:
        steps = file.readlines()
    with open("data/Kitchentools.txt", 'r', encoding='utf-8') as file:
        tools = file.readlines()
        for tool in tools:
            kitchen_tools.append(tool[:-1].lower())

    # print(kitchen_tools)
    result = []
    for step in steps:
        tools_found = set(re.findall('|'.join(kitchen_tools), step))
        for tool in tools_found:
            result.append(tool)

    with open("data/tools.txt", "w", encoding='utf-8') as file:
        for tool in result:
            file.write(f"{tool}\n")

    return result
    # print(result)

def get_actions():
    kitchen_actions = []
    with open("data/steps.txt", 'r', encoding='utf-8') as file:
        steps = file.readlines()
    with open("data/Kitchenactions.txt", 'r', encoding='utf-8') as file:
        actions = file.readlines()
        for action in actions:
            kitchen_actions.append(action[:-1].lower())

    result = []
    for step in steps:
        actions_found = set(re.findall('|'.join(kitchen_actions), step))
        for action in actions_found:
            result.append(action)

    with open("data/actions.txt", "w", encoding='utf-8') as file:
        for action in result:
            file.write(f"{action}\n")
    return result

def get_ingredients():
    with open("data/ingredients.txt", "r", encoding='utf-8') as file:
        return file.read().splitlines() 
    
def get_steps():
    with open("data/steps.txt", "r", encoding='utf-8') as file:
        return file.read().splitlines()

# if __name__ == '__main__':
#     extract_recipe_details("https://www.allrecipes.com/miso-noodle-soup-in-a-jar-recipe-8350566")
#     get_tools("data/steps.txt")

import pdb

import requests
from bs4 import BeautifulSoup


# class Step:
#     def __init__(self, text, url, actions, ingredients, tools):
#         self.text = text
#         self.url = url
#         self.actions = actions
#         self.ingredients = ingredients
#         self.tools = tools


def fetch_recipe_titles_and_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error retrieving page: Status code {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    recipes = []

    for card in soup.find_all("a", class_=lambda value: value and "mntl-card-list-items" in value):
        title_element = card.find("span", class_="card__title-text")
        if title_element:
            title = title_element.text.strip()
            link = card.get('href')
            recipes.append((title, link))

    return recipes


def extract_recipe_details(path):
    recipes_data = {}

    with open('data/recipes_links.txt', 'r', encoding='utf-8') as files:
        lines = files.readlines()

        for line in lines:
            recipes_data[line.split('&&')[0]] = line.split('&&')[1]

        # print(recipes_data)
        fetched_recipes = {}
        # pdb.set_trace()

        for title in recipes_data.keys():
            response = requests.get(recipes_data[title])
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                recipe_content = soup.find("div", class_="recipe-content")
                if recipe_content:
                    fetched_recipes[title] = recipe_content.get_text(strip=True)
            else:
                print(f"Error retrieving recipe for {title}: Status code {response.status_code}")


if __name__ == '__main__':
    recipes = fetch_recipe_titles_and_links('https://www.allrecipes.com')
    for title, link in recipes:
        print(f"Recipe: {title} - Link: {link}")

    output_file_path = 'data/recipes_links.txt'
    with open(output_file_path, 'w') as file:
        for title, link in recipes:
            file.write(f"{title} && {link}\n")

    extract_recipe_details('data/recipes_links.txt')

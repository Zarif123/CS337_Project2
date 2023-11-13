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

def extract_recipe_details(url):

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error retrieving page: Status code {response.status_code}")
        return None

    # pdb.set_trace()
    soup = BeautifulSoup(response.content, 'html.parser')

    # 找到所有食材列表项
    ingredients_list_items = soup.find_all("li", class_="mntl-structured-ingredients__list-item")

    # 提取食材的数量、单位和名称
    ingredients = []
    for item in ingredients_list_items:
        quantity = item.find("span", {"data-ingredient-quantity": "true"}).get_text(strip=True)
        unit = item.find("span", {"data-ingredient-unit": "true"}).get_text(strip=True)
        name = item.find("span", {"data-ingredient-name": "true"}).get_text(strip=True)
        ingredients.append(f"{quantity} {unit} {name}".strip())

    steps = []
    steps_items = soup.find_all('p',  class_="comp mntl-sc-block mntl-sc-block-html")
    for item in steps_items:
        steps.append(item.get_text(strip=True))

    print(ingredients)
    print('-----------------------')
    print(steps)


if __name__ == '__main__':
    # recipes = fetch_recipe_titles_and_links('https://www.allrecipes.com')
    # for title, link in recipes:
    #     print(f"Recipe: {title} - Link: {link}")

    # output_file_path = 'data/recipes_links.txt'
    # with open(output_file_path, 'w') as file:
    #     for title, link in recipes:
    #         file.write(f"{title} && {link}\n")

    url = "https://www.allrecipes.com/recipe/262717/indian-chole-aloo-tikki/"
    extract_recipe_details(url)

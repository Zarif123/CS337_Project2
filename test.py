import requests
from bs4 import BeautifulSoup
import spacy  # 引入自然语言处理库

# 加载spaCy的英语模型
nlp = spacy.load("en_core_web_sm")

class Step:
    def __init__(self, text, actions, ingredients, tools):
        self.text = text
        self.actions = actions
        self.ingredients = ingredients
        self.tools = tools

def extract_info_from_step(step_text):
    """从步骤文本中提取动作、食材和工具/参数"""
    doc = nlp(step_text)
    actions = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    ingredients = [token.text for token in doc if token.dep_ == "dobj"]
    tools = [token.text for token in doc if token.dep_ == "pobj"]
    return actions, ingredients, tools

def fetch_recipes(url, max_pages=5):
    recipes = []

    for page in range(1, max_pages + 1):
        page_url = f"{url}?page={page}"
        response = requests.get(page_url)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        recipe_elements = soup.find_all("article", class_="recipe-article")

        for recipe_element in recipe_elements:
            steps = []
            step_elements = recipe_element.find_all("li", class_="step")  # 假设步骤在<li>标签中

            for step_element in step_elements:
                step_text = step_element.get_text().strip()
                actions, ingredients, tools = extract_info_from_step(step_text)
                step = Step(step_text, actions, ingredients, tools)
                steps.append(step)

            # 这里可以添加代码将步骤（steps）添加到食谱对象中

    return recipes


with open('data/recipes_links.txt', 'r', encoding='utf-8') as files:
    lines = files.readlines()

    for line in lines:
        print(line.split())

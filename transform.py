import re
from helper_constants import *
from helper_functions import *

def transform(chat):
    # Transform patterns
    change_size_pattern = re.compile(r'\b\s*the recipe\s*\b', re.IGNORECASE)
    veg_pattern = re.compile('\b\s*vegetarian\s*\b', re.IGNORECASE)
    chinese_pattern = re.compile('\b\s*chinese\s*\b', re.IGNORECASE)

    if change_size_pattern.search(chat):
        frac = chat.split()[0]
        try:
            frac = fractional_words[frac]
        except:
            frac = float(frac)

        with open("data/ingredients.txt", "r", encoding='utf-8') as file:
            ingredients = file.readlines()
        ingredients = replace_numbers(ingredients, frac)
        with open("data/ingredients.txt", 'w', encoding='utf-8') as file:
            for ing in ingredients:
                file.write(f"{ing}")

        print("I've changed the serving size of the recipe!")
        view_list(get_ingredients())
from step import *
from scraper import *
from helper_functions import *

def main():
    query = ""
    ingredients, steps, tools, actions = "", "", "", ""
    asking_url = True
    print("Hello, if you give me a URL for a recipe from AllRecipes.com, I can walk you through it!")
    while asking_url:
        url = "https://www.allrecipes.com/recipe/281219/skillet-chicken-thighs-with-carrots-and-potatoes/"#input("Please specify your URL here: ")
        if extract_recipe_details(url) == False:
            print("Uh oh there was an error retrieving your recipe, please enter a valid url!")
            continue
        else:
            ingredients = get_ingredients()
            steps = get_steps()
            tools = get_tools()
            actions = get_actions()

            print("I've retrieved your recipe! What would you like me to do?")
            asking_url = False

    in_query_mode = True
    while in_query_mode:
        print("\n1 - View the ingredients")
        print("2 - View the steps")
        print("3 - View the tools needed")
        print("4 - View the actions performed")
        print("5 - Step through the recipe")
        print("6 - Transform the recipe")
        print("7 - Free form chat (Accepts less structured queries)")

        query = input("You can select the corresponding number for each query\n")
        if query == "1":
            print("\nHere are the ingredients:")
            view_list(ingredients)
        elif query == "2":
            print("\nHere are the steps:")
            view_list(steps)
        elif query == "3":
            print("\nHere are the tools:")
            view_list(tools)
        elif query == "4":
            print("\nHere are the actions:")
            view_list(actions)
        elif query == "5":
            print("\nI can help you walk through the steps here!")
            step(ingredients, steps, tools, actions)
        elif query == "6":
            print('\nI can help you transform the recipe!')
            print("You can change the serving size by saying: [halve, double, triple, quadruple, (any float)] the recipe")
            print("You can make the recipe vegetarian by saying: make it vegetarian")
            print("You can make the recipe use Chinese ingredients by saying: make it Chinese")
            transform_type = input("\nHow would you like to transform the recipe?\n")
            transform(transform_type)
        elif query == "7":
            print("\nYou've enabled free form chat!")
            print("You type out questions in sentences rather than entering numbers now")
            in_query_mode = False
        else:
            print("Please enter a valid query")
            continue
    
    in_chat_mode = True
    while in_chat_mode:
        chat = input("\nHow can I assist you?\n")
        search_patterns(chat, ingredients, steps, tools, actions)

if __name__ == "__main__":
    main()

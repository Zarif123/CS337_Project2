from step import *
from scraper import *
from helper_functions import *

def main():
    query = ""
    ingredients, steps, tools, actions = "", "", "", ""
    asking_url = True
    print("Hello, if you give me a URL for a recipe from AllRecipes.com, I can walk you through it!")
    while asking_url:
        url = input("Please specify your URL here: ")
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
        print("1 - View the ingredients")
        print("2 - View the steps")
        print("3 - View the tools needed")
        print("4 - View the actions performed")
        print("5 - Step through the recipe")
        print("6 - Free form chat (Accepts less structured queries)")

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
            print("\nstepping through the recipe")
        elif query == "6":
            print("\nYou've enabled free form chat!")
            print("You type out questions in sentences rather than entering numbers now")
            in_query_mode = False
        else:
            print("Please enter a valid query")
            continue
    
    in_chat_mode = True
    while in_chat_mode:

        # Search patterns
        show_pattern = re.compile(r'\bshow\b', re.IGNORECASE)
        ingredients_pattern = re.compile(r'\bingredients\b', re.IGNORECASE)
        tools_pattern = re.compile(r'\btools\b', re.IGNORECASE)
        actions_pattern = re.compile(r'\bactions\b', re.IGNORECASE)
        steps_pattern = re.compile(r'\bsteps\b', re.IGNORECASE)

        chat = input("\nHow can I assist you?\n")
        if show_pattern.search(chat):
            if ingredients_pattern.search(chat):
                print("\nHere I'll show you the ingredients list:")
                view_list(ingredients)
            elif tools_pattern.search(chat):
                print("\nHere I'll show you the tools list:")
                view_list(tools)
            elif actions_pattern.search(chat):
                print("\nHere I'll show you the actions list:")
                view_list(actions)
            elif steps_pattern.search(chat):
                print("\nHere I'll show you the steps list:")
                view_list(steps)

if __name__ == "__main__":
    main()
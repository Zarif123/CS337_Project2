import re

def view_list(recipe_item):
    for i in recipe_item:
        print(i)

def build_url(query, website):
    formatted_query = "+".join(query.split())
    if website == "youtube":
        template = f"https://www.youtube.com/results?search_query=how+to+{formatted_query}"
    elif website == "google":
        template = f"https://www.google.com/search?q={formatted_query}"
    return template

def search_patterns(chat, ingredients, steps, tools, actions):
    # Search patterns
    show_pattern = re.compile(r'\b(show|what)\b', re.IGNORECASE)
    ingredients_pattern = re.compile(r'\bingredients\b', re.IGNORECASE)
    tools_pattern = re.compile(r'\btools\b', re.IGNORECASE)
    actions_pattern = re.compile(r'\bactions\b', re.IGNORECASE)
    steps_pattern = re.compile(r'\bsteps\b', re.IGNORECASE)

    how_to_pattern = re.compile(r'\bhow (do|can|could) I\b', re.IGNORECASE)
    what_is_pattern = re.compile(r'\bwhat is\b', re.IGNORECASE)

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

    elif how_to_pattern.search(chat):
        how_to_query = chat[how_to_pattern.search(chat).end():]
        print("Here is how you can do that!\n")
        how_to_url = build_url(how_to_query.strip('.?!'), 'youtube')
        print(how_to_url)

    elif what_is_pattern.search(chat):
        print("Here is what I've found!\n")
        format_url = build_url(chat.strip('.?!'), 'google')
        print(format_url)

def step_util(ingredients, steps, tools, actions, stepping):
    index = 0
    print("Here is the first step:")
    print("\n"+steps[index]+"\n")
    while stepping:
        chat = input("\nHow can I assist you?\n")
        search_patterns(chat, ingredients, steps, tools, actions)
        if chat.lower() == "f":
            if index + 1 >= len(steps):
                print("\nYou've reached the end of the recipe")
            else:
                index += 1
                print(steps[index]+"\n")

        elif chat.lower() == "b":
            if index - 1 < 0:
                print('\nCannot go back any further')
            else:
                index -= 1
                print(steps[index]+"\n")

        elif chat.lower() == "q":
            print('\nExiting step mode')
            stepping = False            
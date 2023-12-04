import re
from helper_constants import *

def view_list(recipe_item):
    for i in recipe_item:
        print(i)

def seconds_to_minutes(sec):
    return sec / 60

def replace_numbers(text, frac):
    number_pattern = re.compile(r'\b\d+(\.\d+)?\b')

    for i in range(len(text)):
        found_num = number_pattern.search(text[i])
        if found_num:
            original = found_num.group(0)
            new = str(float(original) * frac)
            text[i] = text[i].replace(original, new)

    return text

def replace_cuisine(text, subs):
    pattern = re.compile('|'.join(subs.keys()), re.IGNORECASE)
    
    for i in range(len(text)):
        found_sub = pattern.search(text[i])
        if found_sub:
            original = found_sub.group(0)
            new = subs[original]
            text[i] = text[i].replace(original, new)

    return text

def build_url(query, website):
    formatted_query = "+".join(query.split())
    if website == "youtube":
        template = f"https://www.youtube.com/results?search_query=how+to+{formatted_query}"
    elif website == "google":
        template = f"https://www.google.com/search?q={formatted_query}"
    return template

def search_list(word, info):
    for token in info:
        if word in token:
            return token
    return False

def search_string(word_list, info):
    for word in word_list:
        for token in info.split():
            if word == token:
                return word
    return False

def get_tools():
    kitchen_tools = []
    with open("data/steps.txt", 'r', encoding='utf-8') as file:
        steps = file.readlines()
    with open("data/Kitchentools.txt", 'r', encoding='utf-8') as file:
        tools = file.readlines()
        for tool in tools:
            kitchen_tools.append(tool[:-1].lower())

    # print(kitchen_tools)
    result = set()
    tool_pattern = re.compile('|'.join(kitchen_tools), re.IGNORECASE)
    for step in steps:
        tools_found = set(tool_pattern.findall(step))
        for tool in tools_found:
            result.add(tool)

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

    result = set()
    action_pattern = re.compile('|'.join(kitchen_actions), re.IGNORECASE)
    for step in steps:
        actions_found = action_pattern.findall(step)
        for action in actions_found:
            result.add(action)

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


def search_patterns(chat, ingredients, steps, tools, actions):
    # Search patterns
    show_pattern = re.compile(r'\b(show|what)(?!\s+is)(?! temperature\b)\b', re.IGNORECASE)
    ingredients_pattern = re.compile(r'\bingredients\b', re.IGNORECASE)
    tools_pattern = re.compile(r'\btools\b', re.IGNORECASE)
    actions_pattern = re.compile(r'\bactions\b', re.IGNORECASE)
    steps_pattern = re.compile(r'\bsteps\b', re.IGNORECASE)

    how_to_pattern = re.compile(r'\bhow (do|can|could) I\b(?!(.*\bthat\b))', re.IGNORECASE)
    what_is_pattern = re.compile(r'\bwhat is\b', re.IGNORECASE)
    how_much_pattern = re.compile(r'\bhow much(?:of\s+)?(.*?)\s+do\b', re.IGNORECASE)

    transform(chat)

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

    elif how_much_pattern.search(chat):
        ingredient = how_much_pattern.search(chat).group(1)
        how_much = search_list(ingredient, ingredients)
        if how_much:
            print("Here is how much you need!\n")
            print(how_much)
        else:
            print("There are no measurments for that in this recipe.\n")

def step_util(ingredients, steps, tools, actions, stepping):
    # Step Patterns
    back_pattern = re.compile(r'\bgo back\b', re.IGNORECASE)
    forward_pattern = re.compile(r'\bgo to the next\b', re.IGNORECASE)
    take_me_pattern = re.compile(r'\bthe\s+(\w+)\s+step\b', re.IGNORECASE)
    ordinal_pattern = re.compile(r'\b(\d+)(st|nd|rd|th)\b', re.IGNORECASE)
    how_long_pattern = re.compile(r'how long?', re.IGNORECASE)
    time_range_pattern = re.compile(r'\b(\d+)\s+to\s+(\d+)\s+(\w+)\b', re.IGNORECASE)
    single_time_pattern = re.compile(fr'\b(\w+)\b(?=\s(?:{"|".join(time_words)}))')
    when_done_pattern = re.compile(r'\bwhen is (it|this) (done|complete|finished)\b', re.IGNORECASE)
    until_pattern = re.compile(r'until (.*?)(?=\.)', re.IGNORECASE)
    how_do_that_pattern = re.compile(r'\bhow (do|can|could) I do that\b', re.IGNORECASE)
    what_temp_pattern = re.compile(r'\bwhat temperature\b', re.IGNORECASE)
    degree_pattern = re.compile(r'(\b\w+\b)\s+degrees\s+(\b\w+\b)', re.IGNORECASE)

    index = 0
    print("Here is the first step:")
    print("\n"+steps[index]+"\n")
    while stepping:
        chat = input("How can I assist you?\n")
        search_patterns(chat, ingredients, steps, tools, actions)
        if chat.lower() == "f" or forward_pattern.search(chat):
            if index + 1 >= len(steps):
                print("\nYou've reached the end of the recipe")
            else:
                index += 1
                print("\n"+steps[index]+"\n")

        elif chat.lower() == "b" or back_pattern.search(chat):
            if index - 1 < 0:
                print('\nCannot go back any further')
            else:
                index -= 1
                print("\n"+steps[index]+"\n")

        elif take_me_pattern.search(chat):
            ordinal_match = ordinal_pattern.search(chat)
            if ordinal_match:
                number = int(ordinal_match.group(1)) - 1
            else:
                number = number_words[take_me_pattern.search(chat).group(1)] - 1
            if number < 0 or number > len(steps):
                print("\nThis is an invalid step number!")
            else:
                index = number
                print("\n"+steps[index]+"\n")

        elif when_done_pattern.search(chat) or how_long_pattern.search(chat):
            until = ""
            total_time = 0
            time_range = time_range_pattern.findall(steps[index])
            for times in time_range:
                try:
                    total_time += ((int(times[0]) + int(times[1])) / 2) * time_map[times[2]]
                except:
                    total_time += 0
                    
            single_times = single_time_pattern.findall(steps[index])
            for times in single_times:
                try:
                    total_time += int(times[0]) * time_map[times[1]]
                except:
                    total_time += 0
            total_time = seconds_to_minutes(total_time)

            until_matches = until_pattern.findall(steps[index])
            if until_matches:
                for match in until_matches:
                    until += "until " + match + '\n'

            print(f"This step takes an average of {total_time} minutes\n")
            if len(until) > 0:
                print(f"{until}")

        elif how_do_that_pattern.search(chat):
            how_do_that_query = "how do I " + steps[index]
            print("Here is what I've found!\n")
            format_url = build_url(how_do_that_query.strip('.?!'), 'google')
            print(format_url)
        
        elif what_temp_pattern.search(chat):
            degrees = degree_pattern.search(chat)
            if degrees:
                num, scale = degrees[0]
                print(f"{num} degrees {scale}\n")
                continue
            else:
                temp = search_string(temperature_words, steps[index])
                if temp:
                    print(f"{temp} heat\n")
                    continue
            print("There is no temperature info for this step.\n")

        elif chat.lower() == "q":
            print('\nExiting step mode')
            stepping = False

def transform(chat):
    # Transform patterns
    change_size_pattern = re.compile(r'\b\s*the recipe\s*\b', re.IGNORECASE)
    veg_pattern = re.compile(r'\b\s*vegetarian\s*\b', re.IGNORECASE)
    chinese_pattern = re.compile(r'\b\s*chinese\s*\b', re.IGNORECASE)
    mexican_pattern = re.compile(r'\b\s*mexican\s*\b', re.IGNORECASE)

    if change_size_pattern.search(chat):
        frac = chat.split()[0]
        try:
            frac = fractional_words[frac]
        except:
            try:
                frac = float(frac)
            except:
                pass
        if type(frac) == float:
            with open("data/ingredients.txt", "r", encoding='utf-8') as file:
                ingredients = file.readlines()
            ingredients = replace_numbers(ingredients, frac)
            with open("data/ingredients.txt", 'w', encoding='utf-8') as file:
                for ing in ingredients:
                    file.write(f"{ing}")

            print("\nI've changed the serving size of the recipe!")
            view_list(get_ingredients())

    elif veg_pattern.search(chat):
        with open("data/ingredients.txt", "r", encoding='utf-8') as file:
            ingredients = file.readlines()
        ingredients = replace_cuisine(ingredients, meat_substitutes)
        with open("data/ingredients.txt", 'w', encoding='utf-8') as file:
            for ing in ingredients:
                file.write(f"{ing}")

        print("\nI've made the recipe vegetarian!")
        view_list(get_ingredients())

    elif chinese_pattern.search(chat):
        with open("data/ingredients.txt", "r", encoding='utf-8') as file:
            ingredients = file.readlines()
        ingredients = replace_cuisine(ingredients, chinese_subs)
        with open("data/ingredients.txt", 'w', encoding='utf-8') as file:
            for ing in ingredients:
                file.write(f"{ing}")

        print("\nI've made the recipe Chinese!")
        view_list(get_ingredients())

    elif mexican_pattern.search(chat):
        with open("data/ingredients.txt", "r", encoding='utf-8') as file:
            ingredients = file.readlines()
        ingredients = replace_cuisine(ingredients, mexican_subs)
        with open("data/ingredients.txt", 'w', encoding='utf-8') as file:
            for ing in ingredients:
                file.write(f"{ing}")

        print("\nI've made the recipe mexican!")
        view_list(get_ingredients())
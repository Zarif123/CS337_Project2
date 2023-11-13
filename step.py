def parse_cooking_action(recipe_step):
    return ""

def parse_tools(recipe_step):
    return ""

def parse_ingredients(recipe_step):
    return ""

def parse_step(recipe_step):
    print(f"Ingredients in this step are: {parse_ingredients(recipe_step)}")
    print(f"Tools in this step are: {parse_tools(recipe_step)}")
    print(f"Cooking actions in this step are: {parse_cooking_action(recipe_step)}")

def step(recipe_steps):
    in_console = True
    index = 0
    while in_console:
        choice = input("Press F to move forward\nPress B to move backward\nPress Q to quit\n")
        if choice.lower() == "f":
            if index + 1 >= len(recipe_steps):
                print("You've reached the end of the recipe")
            index += 1
            print('forward')

        elif choice.lower() == "b":
            if index - 1 < 0:
                print('Cannot go back any further')
                continue
            index -= 1
            print('backward')

        elif choice.lower() == "q":
            print('quitting')
            return
        else:
            print("Please enter a valid option")
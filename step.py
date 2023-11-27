def step():
    recipe_steps = []
    with open("data/steps.txt", "r", encoding='utf-8') as file:
        for step in file.read().splitlines():
            recipe_steps.append(step)
            
    in_console = True
    index = 0
    if len(recipe_steps) > 0:
        print("Here is the first step:\n")
        print(recipe_steps[index])
        while in_console:
            choice = input("\nPress F to move forward\nPress B to move backward\nPress Q to quit\n")
            if choice.lower() == "f":
                if index + 1 >= len(recipe_steps):
                    print("\nYou've reached the end of the recipe")
                    continue
                index += 1
                print("\n"+recipe_steps[index])

            elif choice.lower() == "b":
                if index - 1 < 0:
                    print('\nCannot go back any further')
                    continue
                index -= 1
                print("\n"+recipe_steps[index])

            elif choice.lower() == "q":
                print('\nExiting step mode')
                return
            else:
                print("\nPlease enter a valid option")
    else:
        print("I'm sorry looks like there are no steps!")
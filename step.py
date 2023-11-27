def step():
    recipe_steps = []
    with open("data/steps.txt", "r", encoding='utf-8') as file:
        for step in file.readlines():
            recipe_steps.append(step)
            
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
from helper_functions import *

def step(ingredients, steps, tools, actions):
    # recipe_steps = []
    # with open("data/steps.txt", "r", encoding='utf-8') as file:
    #     for step in file.read().splitlines():
    #         recipe_steps.append(step)
    if len(steps) > 0:
        step_util(ingredients, steps, tools, actions, stepping=True)
    else:
        print("I'm sorry looks like there are no steps!")
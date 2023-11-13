from step import *
def main():
    in_console = True
    query = ""
    while in_console:
        queries = [1,2,3,4]
        print("Queries Available")
        print("1 - View everything in recipe")
        print("2 - View the ingredients")
        print("3 - View the steps")
        print("4 - View the tools")
        print("5 - Step through the recipe")
        query = input("Select the corresponding number for each query")
        if query == "1":
            print("viewing entire recipe")
        if query == "2":
            print("viewing the ingredients")
        if query == "3":
            print("viewing the steps")
        if query == "4":
            print("viewing the tools")
        if query == "5":
            print("stepping through the recipe")
        # For project 3
        # print("Queries Available:")
        # print("1 - View Recipe")
        # print("2 - Dietary Restrictions")
        # print("3 - Healthiness: (healthy meal, don't care)")
        # print("4 - Quantity")
        # print("5 - Cuisine")

        # query = input("Select the corresponding number first")
        # if query == "1":
        #     return #display recipe
        # if query == "2":
        #     diet = input("Select an option from this list (kosher, halal, vegetarian, vegan)")
        # elif query == "3":
        #     health = input("Select an option from this list (healthy, unhealthy)")
        # elif query == "4":
        #     quantity = input("Input any ratio above zero (ex: 0, 0.5, 2, 4)")
        # elif query == "5":
        #     cuisine = input("Select an option from this list (chinese, indian, mexican)")
    return True


if __name__ == "__main__":
    main()
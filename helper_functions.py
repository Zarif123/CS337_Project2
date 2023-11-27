def view_list(recipe_item):
    for i in recipe_item:
        print(i)

def build_url(query):
    formatted_query = "+".join(query.split())
    template = f"https://www.youtube.com/results?search_query={formatted_query}"
    print(template)


build_url("how to preheat an oven")
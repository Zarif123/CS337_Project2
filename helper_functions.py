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
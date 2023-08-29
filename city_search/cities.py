import json

cities = json.load(open('./city_search/cities.json'))

def find_city(name):
    for city in cities:
        if city["name"] == name:
            return city
        
def find_city_incomplete(name):
    namelen = len(name)
    results = []
    if namelen > 2:
        for city in cities:
            if city["name"].lower().startswith(name.lower()):
                results.append(city["name"])
    return results


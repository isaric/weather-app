import json

cities = json.load(open('./city_search/cities.json'))

def find_city(name):
    for city in cities:
        if city["name"] == name:
            return city
        
def find_city_incomplete(name):
    if len(name)<3:
        return []
    results = []
    for city in cities:
        if city["name"].lower().startswith(name.lower()):
            results.append(city["name"])
    return results


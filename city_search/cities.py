import json

cities = json.load(open('./city_search/cities.json'))

def find_city(name):
    for city in cities:
        if city["name"] == name:
            return city


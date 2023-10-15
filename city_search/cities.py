import json

cities = json.load(open('./city_search/cities.json'))

def find_city(lat, lng):
    for city in cities:
        if city["lat"] == lat and city["lng"] == lng:
            return city
        
def find_city_incomplete(name):
    results = []
    for city in cities:
        if city["name"].lower().startswith(name.lower()):
            results.append(city)
    return results


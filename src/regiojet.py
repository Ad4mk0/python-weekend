import requests
import json
import datetime

from src.input_parser import stdin
from src.sqlhandler import db_add, db_get_all, db_to_json
from src.redishandler import save_redis_locations, get_from_redis, set_to_redis

# source, destination, date = stdin()

EURCZK = 25


# gets the id, official name of requested cities

def get_city_id(cityname):
    loc = get_from_redis("mesta")
    if loc == None:
        return
    try:
        res = json.loads(loc)
    except ValueError:
        # if city reference table corrupted, reload it
        save_redis_locations()
        get_city_id(cityname)

    for country in res:
        for cities in country['cities']:
            if cities['name'] == cityname or cityname in cities['aliases']:
                return cities['id'], cities['name']
    raise Exception("city not found")


def get_routes(city1, city2, date):
    arr = []

    if get_city_id(city1) == None or get_city_id(city1) == None:
        save_redis_locations()

    c1, full_name1 = get_city_id(city1)
    c2, full_name2 = get_city_id(city2)

    # DEKOMPONOVAT
    if (res := get_from_redis(f"{full_name1}-{full_name2}")):  # multilanguage
        print("z redisu")
        return json.loads(res)

    # DEKOMPONOVAT
    if (res := db_get_all(full_name1, full_name2)):
        res = db_to_json(res)

        set_to_redis(f"{full_name1}-{full_name2}", json.dumps(res), 600)
        print("z DB")
        return res

    r = requests.get(
        f"https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple?tariffs=REGULAR&toLocationType=CITY&toLocationId={c2}&fromLocationType=CITY&fromLocationId={c1}&departureDate={date}&currency=CZK")
    r = r.json()
    for route in r['routes']:
        arr.append({

            "departure": route['departureTime'],
            "arrival": route['arrivalTime'],
            "origin": full_name1,
            "destination": full_name2,
            "fare": {
                "amount": float(route['creditPriceFrom']),
                "currency": "CZK"
            },
            "type": route['vehicleTypes'],
            "source_id": route['departureStationId'],
            "destination_id": route['arrivalStationId'],
            "free_seats": route['freeSeatsCount']
        })

        db_add(full_name1, full_name2, route['departureTime'], route['arrivalTime'],
               route['vehicleTypes'], float(route['creditPriceFrom']), "CZK")

    set_to_redis(f"{full_name1}-{full_name2}", json.dumps(arr), 600)
    print("z initial loadu")
    return arr


# get_routes("Bratislava", "Brno", '2022-11-20')


# TODO: db_to_json for chains

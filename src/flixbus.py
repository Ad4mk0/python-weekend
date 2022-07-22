import requests
import json

def get_city_id(cityname):
    loc = requests.get(
        f"https://global.api.flixbus.com/search/autocomplete/cities?q={cityname}&lang=en&country=cs&flixbus_cities_only=false")
    loc = loc.json()
    assert loc[0], "place does not exist"
    return loc[0]['id'], loc[0]['name']


def get_routes(city1, city2, date):
    arr = []
    c1, full_name1 = get_city_id(city1)
    c2, full_name2 = get_city_id(city2)
    r = requests.get(
        f"https://global.api.flixbus.com/search/service/v4/search?from_city_id={c1}&to_city_id={c2}&departure_date={date}&products=%7B%22adult%22%3A1%7D&currency=CZK&locale=cs&search_by=cities&include_after_midnight_rides=1")
    r = r.json()
    for e in r["trips"][0]["results"]:
        ali = r["trips"][0]["results"][e]
        arr.append({
            
            "departure_datetime": ali["departure"]["date"],
            "arrival_datetime": ali["arrival"]["date"],
            "source": full_name1,
            "destination": full_name2,
            "fare": {
                "amount": float(ali["price"]["total"]),
                "currency": "CZK"
            },
            "type": "flixbus",
            #ali["departure"]["provider"],
            "source_id": ali["departure"]["city_id"],
            "destination_id": ali["arrival"]["city_id"],
            "free_seats": ali["available"]["seats"]
        })
    print(json.dumps(arr, indent=4))

get_routes("Варшава", "Praha", '14.06.2022')
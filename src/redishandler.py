from redis import Redis
import requests
import json

host = "redis.pythonweekend.skypicker.com"
password = "a9c7a440-cef7-4de1-92ce-e7f922511c0b"
redis = Redis(host=f"{host}", port=6379, db=0,
              password=f"{password}", decode_responses=True)


def set_to_redis(key, val, time):
    prefix = "mikulasek"
    redis.set(prefix+key, val, ex=time)


def get_from_redis(key):
    prefix = "mikulasek"
    return redis.get(prefix+key)


def save_redis_locations():
    loc = requests.get(
        "https://brn-ybus-pubapi.sa.cz/restapi/consts/locations")
    loc = loc.json()
    set_to_redis("mesta", json.dumps(loc), 3600)
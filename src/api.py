from fastapi import FastAPI
from src.regiojet import get_routes
from fastapi.middleware.cors import CORSMiddleware
# from typing import List

# from fastapi.responses import JSONResponse


app = FastAPI()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/whisper")
def whisper(text: str):
    return [text]


@app.get('/ping')
def ping():
    return 'pong'


@app.get('/search')
def search(origin: str, destination: str, departure:list[int], passengers: int = 1,  arrival_date=None):
    print(">>>>>>>>>>", origin, destination, departure)
    # if not origin or not destination or not departure:
    #     return []

    # return get_routes(origin, destination, departure)

# TODO: make wider filter for the routes
# /search?source=Berlin&destination=Prague&passengers=9&departure_date=2022-11-20&arrival_date=2022-12-15

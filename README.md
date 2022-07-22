# Pythonweekend-ksc22



## About

This code is a solution by one of the participants of Kiwi Python Weekend 2022 in Kosice.
We were creating a small kiwi.com for bus connections.
The goal was to scrape, store, calculate over the data and return it as json response through *FastAPI*. It uses *Redis* for caching, *PostgreSQL* as main data storage and *FastAPI*.

## How to run the code?

The easiest way to run this code is by running it as:


`uvicorn api:app --reload` --> start fast api server

make following request such: ``http://127.0.0.1:8000/search?origin=Berlin&destination=Prague&departure_date=2022-11-20``

**Api will return JSON response accordingly.**
from sqlalchemy import create_engine
from sqlalchemy.orm import aliased
from sqlalchemy.orm.session import Session
from sqlalchemy.pool import NullPool

import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Column, Integer, String, TEXT, FLOAT
from sqlalchemy.dialects.postgresql import TIMESTAMP


Base = declarative_base()


class Journey(Base):
    # name of the table
    __tablename__ = "journeys_mikulasek"
    id = Column(Integer, primary_key=True)
    source = Column(TEXT)
    destination = Column(TEXT)
    departure_datetime = Column(TIMESTAMP)
    arrival_datetime = Column(TIMESTAMP)
    carrier = Column(TEXT)
    vehicle_type = Column(TEXT)
    price = Column(FLOAT)
    currency = Column(String(3))


DATABASE_URL = (
    "postgresql://adam_mikulasek:14bb8d3080674fe79770afcfa9e93f31"
    "@sql.pythonweekend.skypicker.com/pythonweekend"
    "?application_name=adam_mikulasek_local_dev"
)
# echo=True shows debug information
# NullPool closes unused connections immediately
engine = create_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool
)

# Base.metadata.create_all(engine) #initial db creation


def time_convert(s_time):
    g, _ = s_time.split('.')
    return datetime.datetime.strptime(g, "%Y-%m-%dT%H:%M:%S")


def db_is_present(source, dest, departure_d, arrival_d, v_type, price, _):
    with Session(engine) as session:
        res = session.query(Journey).filter(
            Journey.source == source, Journey.destination == dest,
            Journey.departure_datetime == time_convert(departure_d),
            Journey.arrival_datetime == time_convert(arrival_d),
            # Journey.vehicle_type==v_type,
            Journey.price == price
        ).all()
    if res != []:
        return True
    return False


def db_add(source, dest, departure_d, arrival_d, v_type, price, currency="CZK"):
    if db_is_present(source, dest, departure_d, arrival_d, v_type, price, currency) == False:
        journey = Journey(
            source=source,
            destination=dest,
            # poriesit datetimes
            departure_datetime=time_convert(departure_d),
            arrival_datetime=time_convert(arrival_d),
            # carrier="FLIXBUS",
            vehicle_type=v_type,
            price=price,
            currency=currency
        )
        # DB connection will be opened and closed automatically
        with Session(engine) as session:

            # add newly created object to the session
            session.add(journey)
            # execute in the DB
            session.commit()


def db_get_all(source, dest):
    with Session(engine) as session:
        # All objects with price 12
        return session.query(Journey).filter(
            Journey.source == source, Journey.destination == dest
        ).all()


def db_to_json(db_obj):
    arr = []
    for e in db_get_all("Prague", "Brno"):
        arr.append({

            "departure": str(e.departure_datetime),
            "arrival": str(e.arrival_datetime),
            "origin": e.source,
            "destination": e.destination,
            "fare": {
                "amount": float(e.price),
                "currency": e.currency
            },
            "type": e.vehicle_type,
            "source_id": None,
            "destination_id": None,
            "free_seats": None
        })

    return arr


def db_fold():
    leg1 = aliased(Journey, name="leg1")
    leg2 = aliased(Journey, name="leg2")
    with Session(engine) as session:
        result = session.query(
            leg1, leg2
        ).join(
            leg2,
            leg1.destination == leg2.source
        ).all().filter(
            
        )
        for row in result:
            print((
                "found combination: "
                f"{row.leg1.source}-{row.leg1.destination}"
                " + "
                f"{row.leg2.source}-{row.leg2.destination}"
            ))
# db_fold()

# TODO: make db_fold working and change db_to_json apropriately

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from database import engine, Booking


def Insert(Mail,Name,Date,Duration,TableMax,Number):
    """вставка данных в таблицу резервирование"""
    booking=Booking(Mail=Mail,Name=Name,Date=Date,Duration=Duration,TableMax=TableMax,Number=Number)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.add(booking)
        session.commit()


def GetAllDateData(date:str,tableMax:int)->list[Booking]:
    """вывод всего резервироания по дате"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return  session.query(Booking).filter(text(""" "Booking"."Date" >= :x ::timestamp and "Booking"."Date" <  :x ::timestamp + interval '1 day' and "TableMax"= :y """)).params(x=date,y=tableMax)



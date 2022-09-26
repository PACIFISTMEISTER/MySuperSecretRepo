from sqlalchemy import Table, Column, MetaData, Integer, Numeric, create_engine, Text, ForeignKey, BOOLEAN, DateTime, \
    func
from sqlalchemy.orm import declarative_base, relationship, Session, sessionmaker
import psycopg2

engine = create_engine('postgresql+psycopg2://postgres:royalflush228@localhost/Shop')
Base = declarative_base()


# Base1 = declarative_base()

class Logininfo(Base):
    __tablename__ = "LoginDB"
    Id=Column(Integer(),primary_key=True)
    mail = Column(Text())
    password = Column(Text())


class Booking(Base):
    """таблица бронирования"""
    __tablename__ = "Booking"
    Id = Column(Integer(), primary_key=True, index=True)
    Mail = Column(Text())
    Number = Column(Integer())
    Name = Column(Text())
    Date = Column(DateTime())
    Duration = Column(Integer())
    TableMax = Column(Integer())


class Stock(Base):
    """таблица доступных товаров"""
    __tablename__ = "Stock"
    Id = Column(Integer(), primary_key=True, index=True)
    TimesPurchased = Column(Integer())
    Name = Column(Text())
    Price = Column(Numeric(20))
    Picture = Column(Text())
    Type = Column(Text())
    FoodType = Column(Text())
    Nation = Column(Text())
    Description = Column(Text())
    Composition = Column(Text())
    IsFromCheif = Column(BOOLEAN())
    IsOnMain = Column(BOOLEAN())
    # coupones = relationship("Coupones",lazy='subquery')
    discount = relationship("Discount", uselist=False, lazy='subquery',cascade="all, delete",)


class Coupones(Base):
    """таблица купонов"""
    __tablename__ = "Coupones"
    Id = Column(Integer(), primary_key=True, index=True)
    DiscountPercent = Column(Integer())
    Number = Column(Integer())
    # Id_of_product = Column(Integer(), ForeignKey("Stock.Id"))


class Discount(Base):
    """таблица скидок"""
    __tablename__ = "Discount"
    Id = Column(Integer(), primary_key=True, index=True)
    Id_of_product = Column(Integer(), ForeignKey("Stock.Id", ondelete="CASCADE"))
    NewPrice = Column(Numeric(20))
    Start_point = Column(DateTime(), default=func.now())  # , server_default=func.now())
    Duration = Column(DateTime())

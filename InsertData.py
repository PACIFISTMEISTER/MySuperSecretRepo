from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from sqlalchemy.testing import not_in

from database import engine, Stock, Discount, Coupones, Logininfo


def ins():
    """базовый набор данных"""
    Session = sessionmaker(bind=engine)
    session = Session()
    inserters=[
        Stock(
            TimesPurchased=100,
            Price=100,
            FoodType="Drink",
            Name="Chicken",
            Picture="chicken.png",
            Type="Dinner",
            Nation="Chinese",
            Description="Brand New and good looking",
            Composition="Chicken,eggs,salt",
            IsFromCheif=True,
            IsOnMain=False
        ),
        Stock(
            TimesPurchased=10,
            Price=150,
            FoodType="Meat",
            Name="nepali momo",
            Picture="nepali-momo.png",
            Type="Lunch",
            Nation="Italian",
            Description="Steamed dumplings filled with slightly spiced minced meat served with special sauce.",
            Composition="Meat,souce,spicy",
            IsFromCheif=True,
            IsOnMain=True
        ),
        Stock(
            TimesPurchased=100,
            Price=300,
            Name="gorkha-special-chicken",
            Picture="gorkha-special-chicken.png",
            FoodType="Meat",
            Type="Lunch",
            Nation="Italian",
            Description="Boneless chicken marinated in mustard, smoked chilli, herbs and spices slowly cooked in tandoor.",
            Composition="Chicken,chilli,herbs",
            IsFromCheif=True,
            IsOnMain=True
        ),
        Stock(
            TimesPurchased=1,
            Price=300,
            FoodType="Fish",
            Name="lam-tikka",
            Picture="lam-tikka.png",
            Type="Lunch",
            Nation="Chinese",
            Description="Tender pieces of lamb mixed with our own spices and gently cooked in clay oven.",
            Composition="Potatoes,spicies,lamb",
            IsFromCheif=False,
            IsOnMain=True
        ),

    ]
    session.bulk_save_objects(inserters)
    session.commit()
    session.close()
def GetPopularData() ->list[Stock]:
    """вывод популярной даты"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Stock).order_by(Stock.TimesPurchased.desc()).limit(3).all()

#def GetPopularData() -> list[Stock]:
 #   Session = sessionmaker(bind=engine)
  #  session = Session()
   # return session.query(Stock).order_by(Stock.TimesPurchased.desc()).limit(3).all()


def GetData(type:str) -> list[Stock]:
    """вывод даты по типу"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Stock).filter(Stock.Type == type).all()


def GetChiefData() -> list[Stock]:
    """вывод даты с пометкой шефа"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Stock).filter(Stock.IsFromCheif==True).all()


def GetDiscount()  ->list[Stock]:
    """вывод даты со скидкой"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Stock).filter(Stock.discount).all()


def GetAllData(nation=None)  ->list[Stock]:
    """вывод даты с учетом нации"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        if nation is None:
            return session.query(Stock).join(Discount,isouter=True).filter(Discount.Id_of_product == None)
        else:
            return session.query(Stock).join(Discount, isouter=True).filter(Discount.Id_of_product == None,Stock.Nation==nation)


def DeleteFromDiscount(ds:Discount):
    """удаление скидки"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.query(Discount).filter(Discount.Id == ds.Id).delete()
        session.commit()



def GetAllForType(type,nation:str) ->list[Stock]:
    """вывод даты по типу и ннации"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Stock).join(Discount, isouter=True).filter(Discount.Id_of_product == None,Stock.Nation==nation,Stock.FoodType==type)



def GetDiscountForType(type,nation)  ->list[Stock]:
    """скидка для типа с учетом нации"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Stock).filter(Stock.discount, Stock.FoodType==type,Stock.Nation==nation).all()


def GetDiscountForNation(nation)  ->list[Stock]:
    """скидка с учетом нации"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Stock).filter(Stock.discount, Stock.Nation==nation).all()

def GetDataById(id:int)->Stock:
    """данные по айди"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Stock).filter(Stock.Id==id).one()

def GetDataByIds(ids:[int])->[Stock]:
    """вывод данных по айди"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        temp=[]
        for id in ids:
            temp.append(session.query(Stock).filter(Stock.Id == id).one())
        return temp

def UseCoupone(Payment:int,Coupone)->float:
    """применеие купона"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        discount = session.query(Coupones.DiscountPercent).filter(Coupones.Number==Coupone).first()
        print('discount',discount[0])
        print('payment',Payment)
        print((discount[0]*Payment)/100)
        return Payment-(discount[0]*Payment)/100


def AdminData() ->list[Stock]:
    """данные для админки"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Stock).all()


def UpdateWithPhoto(id,name,price,file,type,FoodType,NationType,Description,Composition,fromChief,onMain):
    """обновление данных с фото"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.execute(update(Stock).where(Stock.Id==id).values(Name=name,
                                                             Price=price,
                                                             Picture=file,
                                                             Type=type,
                                                             FoodType=FoodType,
                                                             Nation=NationType,
                                                             Description=Description,
                                                             Composition=Composition,
                                                             IsFromCheif=fromChief,
                                                             IsOnMain=onMain))
        session.commit()

def UpdateWithoutPhoto(id,name,price,type,FoodType,NationType,Description,Composition,fromChief,onMain):
    """обновление данных без фото"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.execute(update(Stock).where(Stock.Id==id).values(Name=name,
                                                             Price=price,
                                                             Type=type,
                                                             FoodType=FoodType,
                                                             Nation=NationType,
                                                             Description=Description,
                                                             Composition=Composition,
                                                             IsFromCheif=fromChief,
                                                             IsOnMain=onMain))
        session.commit()



def Insert(name,price,file,type,FoodType,NationType,Description,Composition,fromChief,onMain):
    """вставка новых данных"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        temp= Stock(
            TimesPurchased=0,
            Price=price,
            Name=name,
            Picture=file,
            FoodType=FoodType,
            Type=type,
            Nation=NationType,
            Description= Description,
            Composition=Composition,
            IsFromCheif=fromChief,
            IsOnMain=onMain
        )
        session.add(temp)
        session.commit()




def DeleteData(id:int):
    """удаление данных по айди"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.query(Stock).filter(Stock.Id==id).delete()
        session.commit()



def UpdateDiscount(id,price,duration):
    """обновление данных скидки"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        if session.query(Discount).where(Discount.Id_of_product == id).first()==None:
            temp=Discount(
                NewPrice=price,
                Duration=duration[0] + " " + duration[1],
                Id_of_product=id
            )
            session.add(temp)
        else:
            session.execute(update(Discount).where(Discount.Id_of_product == id).values(
                NewPrice=price,
                Duration=duration[0] + " " + duration[1],
            ))
        session.commit()

def DeleteDiscountById(id):
    """удаление скидки по айди"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        st=session.query(Discount).filter(Discount.Id_of_product == id).one()
        session.query(Discount).filter(Discount.Id_of_product == id).delete()
        session.commit()


def InsertWithDiscount(name,price,file,type,FoodType,NationType,Description,Composition,fromChief,onMain,NewPrice,duration:str):
    """встака данных с учетом скидки"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.commit()
        temp= Stock(
                TimesPurchased=0,
                Price=price,
                Name=name,
                Picture=file,
                FoodType=FoodType,
                Type=type,
                Nation=NationType,
                Description= Description,
                Composition=Composition,
                IsFromCheif=fromChief,
                IsOnMain=onMain
            )
        session.add(temp)
        session.commit()
        result=session.refresh(temp)
        print('res',result)
        print('dur',duration)
        #duration=duration[0].split('T')
        disc = Discount(
            NewPrice=NewPrice[0],
            Duration=duration[0] + " " + duration[1],
            Id_of_product=temp.Id
        )
        session.add(disc)
        session.commit()

def GetCoupones():
    """вствка купонов"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Coupones).all()


def DeleteCoupone(id:int):
    """удаление купона"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.query(Coupones).filter(Coupones.Id==id).delete()
        session.commit()

def ChangeCoupones(id,NewPercent,NewNumber):
    """изменеие данных купона"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.execute(update(Coupones).where(Coupones.Id == id).values(
            DiscountPercent=NewPercent,
            Number=NewNumber
        ))
        session.commit()

def AddCoupones(NewPrice,NewNumber):
    """добавление купона"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        temp=Coupones(
            DiscountPercent=NewPrice,
            Number=NewNumber
        )
        session.add(temp)
        session.commit()

def AddAdmin(login,password):
    """добавление админа"""
    Session=sessionmaker(bind=engine)
    with Session() as session:
        temp=Logininfo(
            mail=login,
            password=password
        )
        session.add(temp)
        session.commit()

def GetPassword(mail:str)->str:
    """извлечение пароля из базы по логину"""
    Session=sessionmaker(bind=engine)
    with Session() as session:
        log=session.query(Logininfo).filter(Logininfo.mail==mail)
        if log==None:
            return "no password detected"
        else:
            return log[0].password

def AddAmount(ids:[int]):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        for id in ids:
            session.query(Stock).filter(Stock.Id == id).update({Stock.TimesPurchased:Stock.TimesPurchased+1})
            session.commit()


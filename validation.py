from datetime import datetime, timedelta

from BookingDB import GetAllDateData


def Validate(mail, name, date, time, duration, number, tableMax):
    """валидация"""
    ValidMail = CheckEmail(mail)
    ValidName = CheckName(name)
    ValidDate = CheckDate(date, time, duration, tableMax)
    ValidNumber = CheckNumber(number)
    return ValidMail == ValidName == ValidDate == ValidNumber == True


def CheckEmail(mail: str):
    """проврека емеил"""
    return True


def CheckName(name: str):
    """проврека имени"""
    if isinstance(name, str) and len(name) < 40:
        return True
    else:
        return False


def CheckDate(date, time, duration, tableMax):
    """провекрка даты"""
    ALlDateData = GetAllDateData(date, tableMax)
    Mydate = date + " " + time + ":00"
    MyDateStart = datetime.strptime(Mydate, "%Y-%m-%d %H:%M:%S")
    delta = timedelta(hours=int(duration))
    MyDateEnd = MyDateStart + delta
    for dat in ALlDateData:
        startdat = dat.Date
        deltaDat = timedelta(hours=dat.Duration)
        enddat = dat.Date + deltaDat
        if MyDateEnd <= startdat or MyDateStart >= enddat:
            print("startdate" + str(startdat), " enddat" + str(enddat) + " ", True)
        else:
            print("startdate" + str(startdat), " enddat" + str(enddat) + " ", False)
            return False
    return True


def CheckNumber(number):
    """проверка номера"""
    try:
        num = int(number)
    except:
        return False
    if num < 99999999:
        return True
    return False


def CheckCoupone(Coupone):
    """проверка купона"""
    if len(Coupone) != 4:
        return False
    return True


def ValidatePayment(mail: str, Coupone):
    """проврека для оплаты"""
    return CheckEmail(mail) == CheckCoupone(Coupone) == True


def DataValidate(name, price, Description, Composition, timer):
    return CheckName(name) == CheckPrice(price) == CheckDescription(Description) == CheckComposition(
        Composition) == CheckTimer(timer) == True


def CheckPrice(price):
    try:
        num = int(price)
    except:
        return False
    if num < 99999999:
        return True
    return False


def CheckDescription(Description):
    if len(Description) < 100:
        return True
    return False


def CheckComposition(Composition):
    if len(Composition) < 50:
        return True
    return False


def CheckTimer(timer):
    print('timer', timer)
    if timer is not None:
        try:
            mydate = datetime.strptime(timer[0], '%Y-%m-%d')
            if mydate > (datetime.today() + timedelta(days=365)):
                return False
        except:
            return False
    return True

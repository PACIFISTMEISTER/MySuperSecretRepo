from flask import Blueprint, render_template,redirect

from InsertData import  GetDiscountForType, GetAllData, GetDiscountForNation, GetAllForType

chinese_food=Blueprint("/", __name__, static_folder="static", template_folder="templates")

@chinese_food.route("/")
def ShowAll():
    """вывод всей китайской еды"""
    AllData=GetAllData(nation="Chinese")
    DiscountData = GetDiscountForNation("Chinese")
    return render_template("chinese.html",AllData=AllData,DiscountData=DiscountData)


@chinese_food.route("/<type>")
def ShowFood(type):
    """вывод всей китайской еды с учетом типа"""
    DiscountData=GetDiscountForType(type=type,nation="Chinese")
    AllData=GetAllForType(type=type,nation="Chinese")
    return render_template("chinese.html",DiscountData=DiscountData,AllData=AllData)

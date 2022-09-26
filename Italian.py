from flask import Blueprint, render_template,redirect

from InsertData import  GetDiscountForType, GetAllData, GetDiscountForNation, GetAllForType

italian_food=Blueprint("/", __name__, static_folder="static", template_folder="templates")

@italian_food.route("/")
def ShowAll():
    """итальянская еда"""
    AllData=GetAllData(nation="Italian")
    DiscountData = GetDiscountForNation("Italian")
    return render_template("italian.html",AllData=AllData,DiscountData=DiscountData)


@italian_food.route("/<type>")
def ShowFood(type):
    """итальянская еда с учетом типа"""
    DiscountData=GetDiscountForType(type=type,nation="Italian")
    AllData=GetAllForType(type=type,nation="Italian")
    return render_template("italian.html",DiscountData=DiscountData,AllData=AllData)

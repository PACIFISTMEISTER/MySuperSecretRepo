from datetime import datetime

from flask import Blueprint, render_template

from InsertData import GetDiscount, GetAllData, GetPopularData, DeleteFromDiscount

menu_page = Blueprint("menu_page", __name__, static_folder="static", template_folder="templates")


@menu_page.route("/")
def menu():
    """вывод меню"""
    PopularData = GetPopularData()
    DiscountData=GetDiscount()
    for data in DiscountData:
        if data.discount.Duration<datetime.now(tz=None):
            DiscountData.remove(data)
            DeleteFromDiscount(data)
    AllData=GetAllData()

    return render_template("menu.html", DiscountData=DiscountData,AllData=AllData,PopularData=PopularData)

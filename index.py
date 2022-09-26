from flask import Blueprint, render_template

from InsertData import GetPopularData, GetData, GetChiefData, ins

index_page = Blueprint("index", __name__, static_folder="static", template_folder="templates")


@index_page.route('/')
def index():
    """вывод главной страницы"""
    PopularData = GetPopularData()
    LunchData = GetData("Lunch")
    #for data in LunchData:
      #  if data.discount!=None:
       #     data.Price=data.discount.NewPrice
    ChiefData = GetChiefData()

   # for data in ChiefData:
      #  if data.discount!=None:
       #     data.Price=data.discount.NewPrice
    return render_template("index.html", PopularData=PopularData, LunchData=LunchData, BreakFastData=LunchData,DinnerData=LunchData,ChiefData=ChiefData,FooterData=PopularData)

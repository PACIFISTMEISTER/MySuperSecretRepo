import os
from datetime import datetime

from flask import Blueprint, render_template, redirect, request
from flask.views import MethodView
from flask_cors import CORS
from werkzeug.utils import secure_filename

from InsertData import AdminData, UpdateWithPhoto, UpdateWithoutPhoto, Insert, DeleteData, UpdateDiscount, \
    DeleteDiscountById, InsertWithDiscount, GetCoupones, DeleteCoupone, ChangeCoupones, AddCoupones
from login import CheckLogForClass, CheckLogForFunc
from validation import DataValidate

admin_page = Blueprint("admin_page", __name__, static_folder="static", template_folder="templates")
CORS(admin_page, supports_credentials=True)
upload_dir = "static/images"


class Admin_class(MethodView):
    @CheckLogForClass
    def get(self):
        """вывод старницы админки"""
        allData = AdminData()
        for dat in allData:
            if dat.discount:
                print(dat.discount.Duration)
        today = datetime.now()
        today = today.strftime("%d/%m/%Y %H:%M:%S")
        return render_template("admin.html", allData=allData, Today=today)

    @CheckLogForClass
    def post(self):
        """добавление данных"""
        if "newData" in request.form:

            name = request.form.get("NewName")
            price = request.form.get("NewPrice")
            file = request.files["NewFile"]
            type = request.form.get("NewType")
            FoodType = request.form.get("NewFoodType")
            NationType = request.form.get("NewNation")
            Description = request.form.get("NewDescription")
            Composition = request.form.get("NewCompostion")
            FromChief = request.form.getlist("NewChief")
            OnMain = request.form.getlist("NewMain")
            NewDiscount = request.form.get("NewDiscount")
            timer = NewDiscount.rsplit("T", 1)
            NewDiscountPrice = request.form.getlist("NewDiscountPrice")
            if name and price and Description and Composition and timer and NewDiscountPrice:
                if DataValidate(name,price,Description,Composition,timer) is False:
                    return redirect('/Admin',304)
                if file and file.filename.rsplit('.', 1)[1].lower() == "png":
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(upload_dir, filename))

                    if FromChief == 'on':
                        fromChief = True
                    else:
                        fromChief = False

                    if OnMain == 'on':
                        onMain = True
                    else:
                        onMain = False

                    if NewDiscountPrice and NewDiscount:

                        InsertWithDiscount(name, price, file.filename, type, FoodType, NationType, Description, Composition,
                                           fromChief, onMain, NewDiscountPrice, timer)
                    else:
                        Insert(name, price, file.filename, type, FoodType, NationType, Description, Composition, fromChief,
                               onMain)

                    return redirect("/Admin", 302)
                else:
                    return redirect("/Admin", 302)
        else:
            """изменение данных"""
            id = request.form.get("IdInput")
            name = request.form.get("NameInput")
            price = request.form.get("PriceInput")
            file = request.files["formFile"]
            type = request.form.get("SelectType")
            FoodType = request.form.get("SelectFoodType")
            NationType = request.form.get("NationType")
            Description = request.form.get("DescriptionInput")
            Composition = request.form.get("CompositionInput")
            FromChief = request.form.getlist("FromChief")
            OnMain = request.form.getlist("OnMain")
            NewDiscount = request.form.get("Discount")
            NewDiscountPrice = request.form.get("NewPrice")
            timer = NewDiscount.rsplit("T", 1)
            DeleteDiscount = request.form.getlist("DeleteDiscount")
            if DataValidate(name,price,Description,Composition,timer) is False:
                return redirect('/Admin',304)
            if NewDiscountPrice and timer and id:
                UpdateDiscount(id, NewDiscountPrice, timer)
            if DeleteDiscount and DeleteDiscount[0] == 'on':
                DeleteDiscountById(id)
            else:
                DeleteDiscount = False
            if file and file.filename.rsplit('.', 1)[1] == "png":
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_dir, filename))

                if FromChief and FromChief[0] == 'on':
                    fromChief = True
                else:
                    fromChief = False

                if OnMain and OnMain[0] == 'on':
                    onMain = True
                else:
                    onMain = False
                UpdateWithPhoto(id, name, price, file.filename, type, FoodType, NationType, Description, Composition,
                                fromChief, onMain)
                return redirect("/Admin", 302)
            else:
                if FromChief and FromChief[0] == 'on':
                    fromChief = True
                else:
                    fromChief = False

                if OnMain and OnMain[0] == 'on':
                    onMain = True
                else:
                    onMain = False
                UpdateWithoutPhoto(id, name, price, type, FoodType, NationType, Description, Composition,
                                   fromChief, onMain)
            return redirect("/Admin", 302)


@admin_page.route("/Delete/<int:id>", methods=["DELETE"])
@CheckLogForFunc
def AddData(id):
    """удаление товара"""
    print("im deleting",id)
    DeleteData(id)
    return redirect("/Admin", 301)


admin_page.add_url_rule("/", view_func=Admin_class.as_view("booking"))


class Admin_Coupones(MethodView):
    @CheckLogForClass
    def get(self):
        AllCoupones = GetCoupones()
        return render_template("Coupones.html", AllCoupones=AllCoupones)

    @CheckLogForClass
    def post(self):
        """добавление купона"""
        if 'ChangeData' in request.form:
            id = request.form.get("IdInput")
            NewPercent = request.form.get("PriceInput")
            NewNumber = request.form.get("NewNumber")

            ChangeCoupones(id, NewPercent, NewNumber)
        else:
            """изменеие купона"""
            NewPrice = request.form.get("NewPrice")
            NewNumber = request.form.get("NewNumber")
            AddCoupones(NewPrice, NewNumber)

        return redirect("/Admin/Coupones", 302)


admin_page.add_url_rule("/Coupones", view_func=Admin_Coupones.as_view("Coupones"))


@admin_page.route("/DeleteCoupone/<int:id>", methods=["DELETE"])
@CheckLogForFunc
def Delete(id):
    """удаление купона"""
    DeleteCoupone(id)
    return redirect("/Admin/Coupones", 301)

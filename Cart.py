import flask
from flask import Blueprint, render_template, session, jsonify, request, flash, redirect
from flask_cors import CORS

from InsertData import GetDataById, GetDataByIds, UseCoupone
from OperationOnPayment import SandMail, ClearTable
from validation import ValidatePayment, CheckEmail

cart_path = Blueprint("/", __name__, static_folder="static", template_folder="templates")
CORS(cart_path, supports_credentials=True)


@cart_path.route("/", methods=["GET"])
def ShowCart():
    """вывод корзины"""
    MyCart = []
    Payment = 0

    if 'data' in session:
        print('data',session['data'])
        MyCart = GetDataByIds(session['data'])

        for data in MyCart:
            if data.discount is None:
                Payment = Payment + data.Price
            else:
                Payment = Payment + data.discount.NewPrice
        print(Payment)
        print(session['data'])
    return render_template("Cart.html", CartData=MyCart, Payment=Payment)


@cart_path.route("/", methods=["POST"])
def GetPayment():
    """оплата товара"""
    if 'data' in session:
        mail = request.form.get("EmailInput")
        Coupone = request.form.get("Coupone")
        SelectType = request.form.get("SelectType")
        if Coupone:
            if ValidatePayment(mail, Coupone) == True:
                MyCart = []
                Payment = 0

                MyCart = GetDataByIds(session['data'])

                for data in MyCart:
                    if data.discount is None:
                        Payment = Payment + data.Price
                    else:
                        Payment = Payment + data.discount.NewPrice
                print('Payment',Payment)

                Payment = UseCoupone(Payment, Coupone)
                print('Payment after',Payment)
                if SelectType == "Доставка(от 500)":
                    if Payment < 500:
                        flash("Доставка только от 500 рублей")
                        return redirect("/Cart", 301)
                    else:
                        SandMail(mail,Payment)
                        ClearTable()
                        return redirect("/", 301)
                if SelectType == "К брони":
                    if 'booking' in session:
                        session.pop('booking')
                        SandMail(mail,Payment)
                        ClearTable()
                        return redirect("/", 301)
                    else:
                        flash("Сначала забронируйте")
                        return redirect("/Cart", 301)

                else:
                    SandMail(mail, Payment)
                    ClearTable()
                    return redirect("/Cart", 301)
        if CheckEmail(mail):
            MyCart = []
            Payment = 0

            MyCart = GetDataByIds(session['data'])

            for data in MyCart:
                if data.discount is None:
                    Payment = Payment + data.Price
                else:
                    Payment = Payment + data.discount.NewPrice
            SandMail(mail,Payment)
            ClearTable()
        return redirect("/", 301)
    else:
        return redirect("/",302)


@cart_path.route("/addToCard/<int:id>", methods=["PUT"])
def AddData(id):
    """добавление в корзину"""

    if 'data' in session:
        session['data'].append(id)
        temp = session['data']
        session['data'] = temp
    else:

        session['data'] = []
        session['data'].append(id)
        print('in add data',session['data'])
    return '', 200


@cart_path.route("/DeleteFromToCard/<int:id>", methods=["PUT"])
def DeleteData(id):
    """удаление товара из корзины"""
    if 'data' in session:

        temp = session['data']
        temp.remove(id)
        session['data'] = temp
        print('old', session['data'])

    else:
        session['data'] = []

    return '',200

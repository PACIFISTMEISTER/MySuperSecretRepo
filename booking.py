from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, redirect, flash, session
from flask.views import View, MethodView
from flask_cors import CORS

from BookingDB import Insert
from validation import Validate

booking_page = Blueprint("booking_page", __name__, static_folder="static", template_folder="templates")
CORS(booking_page, supports_credentials=True)


class Booking(MethodView):
    def get(self):
        """вывод страницы резервирования"""
        date = datetime.now().strftime('%Y-%m-%d')
        dateASdt = datetime.strptime(date, "%Y-%m-%d")
        dates = [date.replace("00:00:00", "")]
        for i in range(1, 7):
            delta = timedelta(days=i)
            dat = str(dateASdt + delta).replace("00:00:00", "")
            dates.append(dat)
        return render_template("Booking.html", Date=dates)

    def post(self):
        """резервирование на 2"""
        if "BookForTwo" in request.form:
            mail = request.form.get("EmailInput")
            number = request.form.get("PhoneNumber")
            name = request.form.get("Name")
            date = request.form.get("SelectDate")
            time = request.form.get("SelectTime")
            duration = request.form.get("DurationTime")
            if Validate(mail, name, date, time, duration[0], number, 2) == True:
                session['booking'] = "Booked"
                Insert(mail, name, date + " " + time, duration[0], 2, number)
            else:
                flash("Время уже зарезервировано")


        else:
            """резервирование на 4"""
            if "BookForFour" in request.form:
                mail = request.form.get("EmailInput")
                number = request.form.get("PhoneNumber")
                name = request.form.get("Name")
                date = request.form.get("SelectDate")
                time = request.form.get("SelectTime")
                duration = request.form.get("DurationTime")

                if Validate(mail, name, date, time, duration[0], number, 4) == True:
                    Insert(mail, name, date + " " + time, duration[0], 2, number)
                    session['booking'] = "Booked"
                else:
                    flash("Время уже зарезервировано")

        return redirect("/Booking", 302)


booking_page.add_url_rule("/", view_func=Booking.as_view("booking"))

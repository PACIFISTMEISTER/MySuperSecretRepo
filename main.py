from flask import Flask, render_template
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
import bcrypt

from Cart import cart_path
from Chineese import chinese_food
from InsertData import ins, AddAdmin
from Italian import italian_food
from admin import admin_page
from booking import booking_page
from index import index_page
from database import Base, engine
from login import login_path
from menu import menu_page

app = Flask(__name__)

app.secret_key = "imsupersecret"
app.config['SESSION_COOKIE_SAMESITE'] = "Strict"
app.config['SESSION_COOKIE_SECURE'] = False

CORS(app, supports_credentials=True)
CORS(cart_path, supports_credentials=True, origins=["http://localhost:8080"], headers=['Content-Type'],
     expose_headers=['Access-Control-Allow-Origin'])

app.register_blueprint(index_page, url_prefix="/")
app.register_blueprint(menu_page, url_prefix="/menu")
app.register_blueprint(cart_path, name="cart", url_prefix="/Cart")
app.register_blueprint(login_path, name="login", url_prefix="/Login")
app.register_blueprint(italian_food, name="italian", url_prefix="/italian")
app.register_blueprint(chinese_food, name="chinese", url_prefix="/Chinese")
app.register_blueprint(booking_page, name="booking", url_prefix="/Booking")
app.register_blueprint(admin_page, name="admin", url_prefix="/Admin")

# TODO Добавить чек/статистику в бд


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # app.run(port=8080)
    app.run(port=8080, debug=True)

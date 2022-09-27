from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from Cart import cart_path
from Chineese import chinese_food
from Italian import italian_food
from admin import admin_page
from booking import booking_page
from database import Base, engine
from index import index_page
from login import login_path
from menu import menu_page


class AppFactory:
    app = None

    def ForDebug(self):
        self.app = Flask(__name__)


        self.app.secret_key = "imsupersecret"
        self.app.config['SESSION_COOKIE_SAMESITE'] = "Strict"
        self.app.config['SESSION_COOKIE_SECURE'] = False

        CORS(self.app, supports_credentials=True)
        CORS(cart_path, supports_credentials=True, origins=["http://localhost:8080"], headers=['Content-Type'],
             expose_headers=['Access-Control-Allow-Origin'])

        self.app.register_blueprint(index_page, url_prefix="/")
        self.app.register_blueprint(menu_page, url_prefix="/menu")
        self.app.register_blueprint(cart_path, name="cart", url_prefix="/Cart")
        self.app.register_blueprint(login_path, name="login", url_prefix="/Login")
        self.app.register_blueprint(italian_food, name="italian", url_prefix="/italian")
        self.app.register_blueprint(chinese_food, name="chinese", url_prefix="/Chinese")
        self.app.register_blueprint(booking_page, name="booking", url_prefix="/Booking")
        self.app.register_blueprint(admin_page, name="admin", url_prefix="/Admin")
        Base.metadata.create_all(engine)
        return self.app

    def GetHash(self):
        return Bcrypt(self.app)


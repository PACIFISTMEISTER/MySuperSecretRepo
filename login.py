from flask import Blueprint, request, redirect, render_template, session
from flask.views import MethodView
from flask_cors import CORS
import bcrypt

from InsertData import GetPassword

login_path = Blueprint("/", __name__, static_folder="static", template_folder="templates")
CORS(login_path, supports_credentials=True)


def CheckLogForClass(func):
    """проверка доступа для функций класса"""

    def wrapper(self, *args, **kwargs):
        result = None
        if 'logged' in session:
            if request.path == '/Login/':
                return redirect('/Admin', 302)
            result = func(self, *args, **kwargs)
        else:
            if request.path == '/Login/':
                result = func(self, *args, **kwargs)
            else:
                return redirect('/Login', 302)
        return result

    wrapper.__name__ = func.__name__
    return wrapper

def CheckLogForFunc(func):
    """проверка доступа для функций """

    def wrapper( *args, **kwargs):
        result = None
        if 'logged' in session:
            if request.path == '/Login/':
                return redirect('/Admin', 302)
            result = func( *args, **kwargs)
        else:
            if request.path == '/Login/':
                result = func(*args, **kwargs)
            else:
                return redirect('/Login', 302)
        return result

    wrapper.__name__ = func.__name__
    return wrapper

class Login(MethodView):
    @CheckLogForClass
    def get(self):
        """вывод страницы резервирования"""

        return render_template("login.html")

    @CheckLogForClass
    def post(self):
        """проверка пароля"""
        if 'loginData' in request.form:
            mail = request.form.get("loginInput")
            password = request.form.get("passwordInput")
            hash = GetPassword(mail)
            if hash == "no password detected":
                return redirect('/', 403)
            if bcrypt.checkpw(bytes(password, encoding='utf8'), bytes(hash, encoding='utf8')):
                session['logged'] = True
                return redirect("/Admin", 302)
            else:
                return redirect('/', 403)


@login_path.route("/LogOut")
def logOut():
    """логаут"""
    print("im in logout")
    session.pop('logged', None)
    return '', 200


login_path.add_url_rule("/", view_func=Login.as_view("login"))

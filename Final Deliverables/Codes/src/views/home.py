from flask import Blueprint,render_template
from datetime import datetime as date

home = Blueprint('home',__name__)

@home.route('/')
def index():
    return render_template("index.html")

@home.route('/<username>/<email>/<mobile>/<sno>')
def user(username,email,mobile,sno):
    return render_template("index.html",msg=username,email=email,mobile=mobile,sno=sno,date=date.today().strftime("%A"))

@home.route("/returns/<mobile>")
def returns(mobile):
    return render_template("order.html",mobile=mobile)

@home.route("/cart/<mobile>/")
def cart(mobile):
    return render_template("cart.html",mobile=mobile)
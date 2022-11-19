import ibm_db
from flask import Blueprint,render_template,request
from datetime import datetime

cart = Blueprint("cart",__name__)

@cart.route("/<mobile>/")
def box(mobile):
    return render_template("cart.html",mobile=mobile)
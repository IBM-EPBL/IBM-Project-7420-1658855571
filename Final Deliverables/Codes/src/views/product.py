from flask import Blueprint,render_template,request,redirect,flash,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


product = Blueprint("product",__name__)

@product.route("/<product_name>/<company_name>/<logo>/<product_image>/<price>/<date>/<location>/<rating>/<f1>/<f2>/<f3>/<f4>/<f5>/<username>/<email>/<mobile>/<sno>")
def individual(product_name,company_name,logo,product_image,price,date,location,rating,f1,f2,f3,f4,f5,username,email,mobile,sno):
    logo = url_for('static',filename='/images/'+str(logo))    
    return render_template("product.html",product_name=product_name,username=username,email=email,mobile=mobile,sno=sno,company_name=company_name,logo=logo,product_image=product_image,price=price,date=date,location=location,rate=rating,f1=f1,f2=f2,f3=f3,f4=f4,f5=f5)

@product.route('<username>/<email>/<mobile>/<sno>/Watches')
def watch(username,email,mobile,sno):
    return render_template("watchproduct.html",msg=username,email=email,mobile=mobile,sno=sno)

@product.route('<username>/<email>/<mobile>/<sno>/Clothes')
def clothes(username,email,mobile,sno):
    return render_template("productcloth.html",msg=username,email=email,mobile=mobile,sno=sno)
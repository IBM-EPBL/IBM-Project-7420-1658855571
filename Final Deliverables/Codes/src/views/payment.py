from flask import Blueprint,render_template,request,redirect,flash,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from src.services import dbServices,payServices
import ibm_db
import razorpay

conn = dbServices.conn
client = payServices.pay()
print(conn)
payment = Blueprint("payment",__name__)

def check_exist(sno):
    check_exist = "SELECT * FROM ADDRESSDETAILS1 WHERE CUSTOMERID = ?"
    prep = ibm_db.prepare(conn,check_exist)
    ibm_db.bind_param(prep,1,sno)
    ibm_db.execute(prep)
    innverify = ibm_db.fetch_assoc(prep)
    if innverify:
        delivery = innverify["DELIVERYADDRESS"]
        pin = innverify["PINCODE"]
        city = innverify["CITY"]
        state = innverify["STATE"]
    else:
        delivery=""
        pin=""
        city=""
        state=""
    return delivery,pin,city,state

@payment.route("/<product_name>/<product_image>/<price>/details/<username>/<email>/<mobile>/<sno>/<buy>",methods=['POST','GET'])
def openpay(product_name,product_image,price,username,email,mobile,sno,buy):
    name = username
    phone = mobile
    address,pincode,city,state = check_exist(sno)
    add = address
    pn = pincode
    ci = city
    st = state
    if request.method == 'POST':
        snoo = sno
        username = request.form['name']
        mail = request.form['email']
        mobile = request.form['mobile']
        address = request.form['delivery']
        pincode = request.form['pin']
        state = request.form['state']
        city = request.form['city']
        if not address or not state  or not city:
            username = name
            mail = email
            mobile = phone
            address = add
            pincode = pn
            state = st
            city = ci
            flash("Empty address or state or city content!","error")
        elif len(mobile)!=10:
            username = name
            mail = email
            mobile = phone
            address = add
            pincode = pn
            state = st
            city = ci
            flash("Incorrect mobile number format (REMOVE +91)","error")
        elif not pincode:
            username = name
            mail = email
            mobile = phone
            address = add
            pincode = pn
            state = st
            city = ci
            flash("Empty pincode content!","error")
        else:
            select_main ="SELECT * FROM CUSTOMERDETAILS WHERE SNO = ?"
            prep_select = ibm_db.prepare(conn,select_main)
            ibm_db.bind_param(prep_select,1,sno)
            ibm_db.execute(prep_select)
            verifyfirst =  ibm_db.fetch_assoc(prep_select)
            if verifyfirst:
                update_sql="UPDATE CUSTOMERDETAILS SET USERNAME = ? ,EMAIL = ?, MOBILE_NUMBER = ? WHERE SNO = ?"
                prep_stmt = ibm_db.prepare(conn,update_sql)
                ibm_db.bind_param(prep_stmt,1,username)
                ibm_db.bind_param(prep_stmt,2,mail)
                ibm_db.bind_param(prep_stmt,3,mobile)
                ibm_db.bind_param(prep_stmt,4,snoo)
                ibm_db.execute(prep_stmt)
                select_sql="SELECT * FROM ADDRESSDETAILS1 WHERE CUSTOMERID = ?"
                prep_selectadd = ibm_db.prepare(conn,select_sql)
                ibm_db.bind_param(prep_selectadd,1,snoo)
                ibm_db.execute(prep_selectadd)
                verify = ibm_db.fetch_assoc(prep_selectadd)
                if verify:
                    update_sql = "UPDATE ADDRESSDETAILS1 SET MOBILE_NUMBER= ? ,DELIVERYADDRESS= ?, PINCODE= ?, STATE=?, CITY=?, CHANGED_AT= ? WHERE CUSTOMERID = ?"
                    prep_address = ibm_db.prepare(conn,update_sql)
                    ibm_db.bind_param(prep_address,1,mobile)
                    ibm_db.bind_param(prep_address,2,address)
                    ibm_db.bind_param(prep_address,3,pincode)
                    ibm_db.bind_param(prep_address,4,state)
                    ibm_db.bind_param(prep_address,5,city)
                    ibm_db.bind_param(prep_address,6,datetime.now())
                    ibm_db.bind_param(prep_address,7,snoo)
                    ibm_db.execute(prep_address)
                    flash("Successfully Changed!",category='error')
                else:
                    try:
                        ini = 'INSERT INTO  "YKX60167"."ADDRESSDETAILS1" ("CUSTOMERID","MOBILE_NUMBER","DELIVERYADDRESS","CITY","STATE","PINCODE","CHANGED_AT")VALUES(?,?,?,?,?,?,?);'
                        prepr_insert = ibm_db.prepare(conn,ini)
                        ibm_db.bind_param(prepr_insert,1,snoo)
                        ibm_db.bind_param(prepr_insert,2,mobile)
                        ibm_db.bind_param(prepr_insert,3,address)
                        ibm_db.bind_param(prepr_insert,4,city)
                        ibm_db.bind_param(prepr_insert,5,state)
                        ibm_db.bind_param(prepr_insert,6,pincode)
                        ibm_db.bind_param(prepr_insert,7,datetime.now())
                        ibm_db.execute(prepr_insert)
                        flash("Successfully Changed!",category='error')
                    except Exception as e:
                        print("IBM Error:",e)
                    
            else:
                flash("Customer doesn't exist!",category="error")

    return render_template("details.html",product_name=product_name,product_image=product_image,price=price,username=username,email=email,mobile=mobile,sno=sno,address=address,pincode=pincode,state=state,city=city,buy=buy)

@payment.route("/<product_name>/<product_image>/<price>/paymentby/<username>/<email>/<mobile>/<sno>/")
def paymentready(product_name,product_image,price,username,email,mobile,sno):
    Client = client
    data = { "amount": price+"00", "currency": "INR", "receipt": "#11" }
    print(data)
    payment_details = Client.order.create(data=data)
    return render_template("payment.html",payment_details=payment_details,username=username,product_name=product_name,product_image=product_image,price=price,email=email,mobile=mobile,sno=sno)
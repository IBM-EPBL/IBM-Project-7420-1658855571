from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(20), unique=False, nullable=False)
    Email = db.Column(db.String(20), unique=False, nullable=False)
    passWord = db.Column(db.String(20), nullable=False)
 
    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Name : {self.UserName}, PassWord: {self.passWord}"


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/signin", methods=['POST', 'GET'])
def signin():
    return render_template('signin.html')




@app.route("/signup", methods=['POST', 'GET'])
def signup():
    return render_template('signup.html')
   # if request.method == 'POST':
    #    username = request.form['username']
     #   password = request.form['password']
      #  repassword = request.form['repassword']
       # if password == repassword:
        #    return render_template('signin.html')
        #else:
         #   return redirect(url_for('signup'))

@app.route('/add', methods=["POST"])
def profile():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    if username != '' and email != '' and password is not None:
        p = Profile(UserName=username,Email=email,passWord=password)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('signin'))
    else:
        return redirect('/')

@app.route('/check' , methods=["GET"])
def signinChecker():
        email = request.form.get("email")
        password = request.form.get("password")
        email_data = Profile.query.get(email)
        password_data = Profile.query.get(password)
        if(email_data != 0 and password_data != 0):
            return redirect(url_for('home'))
        else:
            return redirect("/")
migrate = Migrate(app, db)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)

from flask import Flask,render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.crypto import Crypto
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route ("/")
def index():
    return render_template("login_regis.html")

@app.route("/register", methods=["POST"])
def validate_user():
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],
            "password":pw_hash,
        }
        users_id = User.save(data)
        session["users_id"] = users_id
        flash("User created!")
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    data ={
        "email":request.form["email"]
    }
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password,request.form["password"]):
        flash("Invalid Email/Password")
        return redirect("/")

    session["users_id"] = user_in_db.id
    return redirect("/dashboard")



@app.route("/dashboard")
def dashboard():
    if "users_id" not in session: 
        flash("Must be logged in!")
        return redirect("/")
    else:
        data = {
            "users_id":session["users_id"],
        }
        users = User.show_user(data)
        cryptos = Crypto.get_all_cryptos()
        return render_template("dashboard.html", users=users, cryptos=cryptos ) 

# @app.route("/dashboard")
# def dashboard():
#     if "users_id" not in session: 
#         flash("Must be logged in!")
#         return redirect("/")
#     else:
#         data = {
#             "users_id":session["users_id"]
#         }
#         users = User.show_user(data)
#         cryptos = Crypto.get_all_cryptos()
#         return render_template("dashboard.html", users=users, cryptos=cryptos ) 

@app.route("/logout")
def logout():
    session.clear()
    flash("Awesome work today!")
    return redirect("/")
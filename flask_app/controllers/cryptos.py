from flask import Flask,render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.crypto import Crypto
from flask_app.models.user import User


@app.route ("/NewCrypto")
def add_crypto():
    if "users_id" not in session:
        flash("Must be logged in!")
        return redirect("/")
    else:
        users_id=session["users_id"]
        return render_template("new_crypto.html",users_id=users_id)

# --------------------------------------
#populate on same page route
# --------------------------------------
# @app.route("/dashboard/")
# def dashboard_with_crypto():
#     if "users_id" not in session: 
#         flash("Must be logged in!")
#         return redirect("/")
#     else:
#         data = {
#             "users_id":session["users_id"],
#             "cryptos_id":session["cryptos_id"]
#         }
#         users = User.show_user(data)
#         cryptos = Crypto.get_all_cryptos()
#         selected_crypto = Crypto.show_crypto(data)
#         return render_template("dashboard.html", users=users, cryptos=cryptos, sc=selected_crypto ) 

@app.route ("/submitcrypto/<int:user_id>", methods=["POST"])
def submit_crypto(user_id):
    data = {
        "name":request.form["name"],
        "current_price":request.form["current_price"],
        "current_price_date":request.form["current_price_date"],
        "target_price_buy":request.form["target_price_buy"],
        "target_price_buy_date":request.form["target_price_buy_date"],
        "target_price_sell":request.form["target_price_sell"],
        "target_price_sell_date":request.form["target_price_sell_date"],
        "notes":request.form["notes"],
        "user_id":user_id
    }
    if Crypto.validate_crypto(request.form):
        Crypto.save_crypto(data)
        return redirect("/dashboard")
    else:
        return redirect("/NewCrypto")

@app.route("/edit/<int:id>")
def show_crypto(id):
    if "users_id" not in session:
        flash("Must be logged in!")
        return redirect("/")
    else:
        data ={
            "id":id
        }
        
        users_id=session["users_id"]
        one_crypto = Crypto.show_crypto(data)
        return render_template("edit_crypto.html",users_id=users_id,oc=one_crypto)



@app.route ("/updatecrypto/<int:id>", methods=["POST"])
def update_crypto(id):
    data = {
        "name":request.form["name"],
        "current_price":request.form["current_price"],
        "current_price_date":request.form["current_price_date"],
        "target_price_buy":request.form["target_price_buy"],
        "target_price_buy_date":request.form["target_price_buy_date"],
        "target_price_sell":request.form["target_price_sell"],
        "target_price_sell_date":request.form["target_price_sell_date"],
        "notes":request.form["notes"],
        "id":id
    }
    if Crypto.validate_crypto(request.form):
        Crypto.update_crypto(data)
        return redirect("/dashboard")
    else:
        return redirect(f"/edit/{id}")





@app.route("/delete/<int:id>")
def delete_crypto(id):
    if "users_id" not in session:
        flash("Must be logged in!")
        return redirect("/")
    data ={
        "id":id
    }
    Crypto.delete_crypto(data)
    return redirect ("/dashboard")


@app.route ("/resources")
def resources():
    return render_template("resources.html")
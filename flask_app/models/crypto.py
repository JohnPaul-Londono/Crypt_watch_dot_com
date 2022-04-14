from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from datetime import datetime

class Crypto:
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.current_price = data["current_price"]
        self.current_price_date = data["current_price_date"]
        self.target_price_buy = data["target_price_buy"]
        self.target_price_buy_date = data["target_price_buy_date"]
        self.target_price_sell = data["target_price_sell"]
        self.target_price_sell_date = data["target_price_sell_date"]
        self.notes = data["notes"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @staticmethod
    def validate_crypto(crypto):
        is_valid = True
        if len(crypto["name"]) <= 0:  #name
            flash("Name must be at least 1 character long")
            is_valid = False
        if crypto["current_price"] == "": #current price
            flash("Please enter a Current Price")
            is_valid = False
        # elif float(crypto["current_price"]) == 0:
        #     flash("Current Price must not be 0")
        #     is_valid = False
        if len(crypto["current_price_date"]) < 1: #current price date
            flash("You need to choose a Current Price Date.")
            is_valid = False
        if crypto["target_price_buy"] == "": #target price buy
            flash("Please enter a Target Price")
            is_valid = False
        # elif int(crypto["target_price_buy"]) <= 0:
        #     flash("Target Price must be more than 0")
        #     is_valid = False
        if crypto["target_price_sell"] == "": #target price sell
            flash("Please enter a Target Sell Price")
            is_valid = False
        # elif int(crypto["target_price_sell"]) <= 0:
        #     flash("Target Sell Price must be more than 0")
        #     is_valid = False
        if len(crypto["target_price_buy_date"]) < 1: #target price buy date
            flash("You need to choose a Target Buy Price Date.")
            is_valid = False
        if len(crypto["target_price_sell_date"]) < 1: #target price sell date
            flash("You need to choose a Target Price Sell Date.")
            is_valid = False
        return is_valid

    @classmethod
    def save_crypto(cls,data):
        query = "INSERT INTO cryptos (name,current_price,current_price_date,target_price_buy,target_price_sell,target_price_buy_date,target_price_sell_date,notes,user_id) VALUES (%(name)s,%(current_price)s,%(current_price_date)s,%(target_price_buy)s,%(target_price_sell)s,%(target_price_buy_date)s,%(target_price_sell_date)s,%(notes)s,%(user_id)s);"
        return  connectToMySQL("crypto_watch").query_db(query,data)

    @classmethod
    def update_crypto(cls, data):
        query = "UPDATE cryptos SET name=%(name)s,current_price=%(current_price)s,current_price_date=%(current_price_date)s,target_price_buy=%(target_price_buy)s,target_price_sell=%(target_price_sell)s,target_price_buy_date=%(target_price_buy_date)s,target_price_sell_date=%(target_price_sell_date)s,notes=%(notes)s  WHERE id = %(id)s;"
        return connectToMySQL("crypto_watch").query_db(query,data)





    @classmethod
    def get_all_cryptos(cls): #not pulling data because only retrieving information.
        query = "SELECT * FROM users JOIN cryptos ON users.id = cryptos.user_id;"
        results = connectToMySQL("crypto_watch").query_db(query)
        users_cryptos= []

        for uc in results:
            user_instance = User(uc)
            crypto_data ={
                "id":uc["cryptos.id"],
                "name":uc["name"],
                "current_price":uc["current_price"],
                "current_price_date":uc["current_price_date"],
                "target_price_buy":uc["target_price_buy"],
                "target_price_buy_date":uc["target_price_buy_date"],
                "target_price_sell":uc["target_price_sell"],
                "target_price_sell_date":uc["target_price_sell_date"],
                "notes":uc["notes"],
                "created_at":uc["created_at"],
                "updated_at":uc["updated_at"],
                "user_id":uc["user_id"]
            }
            user_instance.name = Crypto(crypto_data)
            users_cryptos.append(user_instance)
        return users_cryptos


    @classmethod
    def show_crypto(cls, data):
        query = "SELECT * FROM cryptos WHERE id = %(id)s"
        results = connectToMySQL("crypto_watch").query_db(query,data)
        return  cls(results[0])



    @classmethod
    def delete_crypto(cls, data):
        query = "DELETE FROM cryptos WHERE id = %(id)s"
        return connectToMySQL("crypto_watch").query_db(query,data)
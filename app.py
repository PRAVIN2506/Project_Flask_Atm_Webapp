import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import CSRFProtect
from werkzeug.security import check_password_hash

from database import get_connection
from atm import ATM

load_dotenv()

app = Flask(__name__)

# Set SECRET_KEY in your .env file for anything beyond local development.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

csrf = CSRFProtect(app)


@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        account_number = request.form["account_number"]
        pin = request.form["pin"]

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE account_number = %s"

        cursor.execute(query, (account_number,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(user["pin"], pin):
            session["user_id"] = user["id"]
            session["name"] = user["name"]

            return redirect(url_for("dashboard"))
        else:
            error = "Invalid account number or PIN. Please try again."

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        name=session["name"]
    )


@app.route("/balance")
def balance():

    if "user_id" not in session:
        return redirect(url_for("login"))

    atm = ATM(session["user_id"])

    balance = atm.get_balance()

    return render_template(
        "balance.html",
        balance=balance
    )


@app.route("/deposit", methods=["GET", "POST"])
def deposit():

    if "user_id" not in session:
        return redirect(url_for("login"))

    error = None

    if request.method == "POST":

        try:
            amount = float(request.form["amount"])

            atm = ATM(session["user_id"])

            atm.deposit(amount)

            return redirect(url_for("balance"))

        except ValueError as e:
            error = str(e)

    return render_template("deposit.html", error=error)


@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():

    if "user_id" not in session:
        return redirect(url_for("login"))

    error = None

    if request.method == "POST":

        try:
            amount = float(request.form["amount"])

            atm = ATM(session["user_id"])

            atm.withdraw(amount)

            return redirect(url_for("balance"))

        except ValueError as e:
            error = str(e)

    return render_template("withdraw.html", error=error)


@app.route("/transactions")
def transactions():

    if "user_id" not in session:
        return redirect(url_for("login"))

    atm = ATM(session["user_id"])

    transaction_list = atm.get_transactions()

    return render_template(
        "transactions.html",
        transactions=transaction_list
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode)

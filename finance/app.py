import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    username = session.get('username')

    # Complete the implementation of index in such a way that it displays an HTML table summarizing,
    # for the user currently logged in, which stocks the user owns, the numbers of shares owned,
    stock_list = db.execute(
        "SELECT stock, SUM(shares) AS total FROM portfolios WHERE user_id=? GROUP BY stock HAVING total > 0",
        session["user_id"]
    )

    # the current price of each stock, and the total value of each holding (i.e., shares times price).
    prices=[]
    for i in range(len(stock_list)):
        prices.append(usd(lookup(stock_list[i]["stock"]).get('price')))

    totals=[]
    for i in range(len(stock_list)):
        totals.append(usd(lookup(stock_list[i]["stock"]).get('price') * stock_list[i]["total"]))

    zipped = zip(stock_list, prices, totals)

    # Also display the user’s current cash balance along with a grand total (i.e., stocks’ total value plus cash).
    cash = usd(db.execute(
        "SELECT cash FROM users WHERE id=?", session["user_id"]
    )[0]["cash"])

    total = float(cash.replace("$", "").replace(",", ""));
    for i in range(len(totals)):
        total+=float(totals[i].replace("$", "").replace(",", ""))
    total = usd(total)

    return render_template("index.html", username=username, zipped=zipped, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # Get username for header
    username = session.get('username')

    if request.method == "POST":
    # Require that a user input a stock’s symbol, implemented as a text field whose name is symbol.
    # Render an apology if the input is blank or the symbol does not exist (as per the return value of lookup).
        if not request.form.get("symbol") or lookup(request.form.get("symbol")) == None:
            return apology("Must provide valid stock symbol", 400)

    # Require that a user input a number of shares, implemented as a text field whose name is shares.
    # Render an apology if the input is not a positive integer.
        if not request.form.get("shares") or not request.form.get("shares").isdigit() or int(request.form.get("shares")) < 0 or "." in request.form.get("shares"):
            return apology("Must provide a valid number of shares", 400)

    # Submit the user’s input via POST to /buy.
    # Odds are you’ll want to call lookup to look up a stock’s current price.
        price = lookup(request.form.get("symbol")).get('price')
        shares = int(request.form.get("shares"))
        stock = request.form.get("symbol").upper()

    # Odds are you’ll want to SELECT how much cash the user currently has in users.
        cash_db = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )
        cash = float(cash_db[0]["cash"])

    # Render an apology, without completing a purchase, if the user cannot afford the number of shares at the current price.
    # You don’t need to worry about race conditions (or use transactions).
        if (price * shares) > cash:
            return apology("You don't have enough money to purchase that amount", 400)

    # Once you’ve implemented buy correctly, you should be able to see users’ purchases in your new table(s) via phpLiteAdmin or sqlite3.
        # Add purchase to portfolios db
        db.execute(
            "INSERT INTO portfolios (user_id, stock, shares, price, was_bought, date) VALUES(?, ?, ?, ?, TRUE, CURRENT_TIMESTAMP)",
            session["user_id"], stock, shares, price
        )
        # Take money from cash in users db
        db.execute(
            "UPDATE users SET cash = cash - (? * ?) WHERE id = ?",
            shares, price, session["user_id"]
        )

    # Upon completion, redirect the user to the home page.
        return redirect("/")

    else:
        return render_template("buy.html", username=username)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    username = session.get('username')

    # Complete the implementation of history in such a way that it displays an HTML table summarizing
    # all of a user’s transactions ever, listing row by row each and every buy and every sell.
    history = db.execute(
        "SELECT stock, shares, price, was_bought, date FROM portfolios WHERE user_id=?",
        session["user_id"]
    )

    return render_template("history.html", history=history, username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username").lower()
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = request.form.get("username")
        username = session.get('username')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # Get username for header
    username = session.get('username')

    if request.method == "POST":
        # Require that a user input a stock’s symbol, implemented as a text field whose name is symbol.
        if not request.form.get("symbol"):
            return apology("must provide a stock symbol", 400)

    # Submit the user’s input via POST to /quote.
    # In response to a POST, quote can render that second template, embedding within it one or more values from lookup.
        if lookup(request.form.get("symbol")) != None:
            name = lookup(request.form.get("symbol")).get('name')
            symbol = lookup(request.form.get("symbol")).get('symbol')
            price = usd(lookup(request.form.get("symbol")).get('price'))
            return render_template("quoted.html", username=username, name=name, symbol=symbol, price=price)
    # If lookup returns none, give an error
        else:
            return apology("Invalid Stock Symbol", 400)

    # When a user visits /quote via GET, render one of those templates, inside of which should be an HTML
    # form that submits to /quote via POST.

    else:
        return render_template("quote.html", username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username = session.get('username')

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password verification was submitted
        elif not request.form.get("confirmation"):
            return apology("must verify password", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username").lower()
        )

        # Ensure username does not exist
        if len(rows) != 0:
            return apology("Username is already taken", 400)

        # Add user to database
        username = request.form.get("username").lower()
        hash = generate_password_hash(request.form.get("password"))

        if len(rows) == 0:
            db.execute(
                "INSERT INTO users (username, hash) VALUES(?, ?)", username, hash
            )
            user_id = db.execute(
                "SELECT id FROM users WHERE username = ?", username
            )

        # Log user in
        session.clear()
        session["user_id"] = user_id[0]["id"]
        session["username"] = request.form.get("username")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html", username=username)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    username = session.get('username')
    # Complete the implementation of sell in such a way that it enables a user to sell shares of a stock (that he or she owns).
    # Require that a user input a stock’s symbol, implemented as a select menu whose name is symbol.

    stock_list_db = db.execute(
        "SELECT stock, SUM(shares) AS total FROM portfolios WHERE user_id=? GROUP BY stock HAVING total > 0",
        session["user_id"]
    )
    stock_list = [item['stock'] for item in stock_list_db]

    if request.method == "POST":

    # creating needed variables
        shares = int(request.form.get("shares"))
        stock = request.form.get("symbol")
        price = lookup(stock).get('price')

        total_shares = 0
        for name in stock_list_db:
            if name["stock"] == stock:
                total_shares+= name["total"]
                break

    # Render an apology if the user fails to select a stock or if (somehow, once submitted) the user does not own any shares of that stock.
        if not request.form.get("symbol") or request.form.get("symbol") not in stock_list:
            return apology("Please select a stock that you own", 400)

    # Require that a user input a number of shares, implemented as a text field whose name is shares.
    # Render an apology if the input is not a positive integer or if the user does not own that many shares of the stock.
        if not request.form.get("shares") or shares > total_shares:
            return apology("Please enter a valid number of shares", 400)

    # Submit the user’s input via POST to /sell.
        else:
            # add cash value to cash
            db.execute(
                "UPDATE users SET cash = cash + (? * ?) WHERE id = ?",
                shares, price, session["user_id"]
            )

            # create a portfolio entry with shares as a negative number and was_bought as FALSE
            db.execute(
                "INSERT INTO portfolios (user_id, stock, shares, price, was_bought, date) VALUES(?, ?, ?, ?, FALSE, CURRENT_TIMESTAMP)",
                session["user_id"], stock, -abs(shares), price
            )
    # Upon completion, redirect the user to the home page.
            return redirect("/")

    else:
        return render_template("sell.html", stock_list=stock_list, username=username)

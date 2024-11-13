from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

#format function taken from pset 9 - finance
def usd(value):
    """Format value as USD."""
    return f"${float(value):,.2f}"

# Custom filter taken from pset 9 - finance
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database - borrowed from pset 9 - finance
db = SQL("sqlite:///cash-count.db")

# borrowed from pset 9 - finance
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# function borrowed from pset 9 finance
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# code taken from pset 9 - finance
def apology(message, code=400):
    """Render message as an apology to user."""
    first_name = session.get('first_name')

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s
    username = session.get('first_name')
    return render_template("apology.html", top=code, bottom=escape(message), first_name=first_name), code


@app.route("/")
@login_required
def hello_world():
    first_name = session.get('first_name')
    #date format help from the duck
    history = db.execute(
        "SELECT user_id, id, register, date, time, variance FROM history WHERE DATE(date) = DATE('now') ORDER BY date DESC, time DESC"
    )

    var = db.execute(
        "SELECT SUM(variance) FROM history WHERE DATE(date) = DATE('now')"
    )
    # help from the duck to figure out how to pass the sum
    sum_variance=var[0]['SUM(variance)']
    print("print", sum_variance)

    return render_template("index.html", history=history, sum_variance=sum_variance, first_name=first_name)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    first_name = session.get('first_name')

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure first and last name was submitted
        if not request.form.get("first_name"):
            return apology("must provide First Name", 400)

        elif not request.form.get("last_name"):
            return apology("must provide Last Name", 400)

        # Ensure employee id was submitted
        elif not request.form.get("employee_id"):
            return apology("must provide Employee ID", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password verification was submitted
        elif not request.form.get("confirmation"):
            return apology("must verify password", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Query database for employee_id
        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", request.form.get("employee_id")
        )

        # Ensure username does not exist
        if len(rows) != 0:
            return apology("Employee is already registered", 400)

        # Add user to database
        employee_id = request.form.get("employee_id")
        hash = generate_password_hash(request.form.get("password"))
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        if len(rows) == 0:
            db.execute(
                "INSERT INTO users (id, first_name, last_name, hash) VALUES(?, ?, ?, ?)", employee_id, first_name, last_name, hash
            )
            user_id = db.execute(
                "SELECT * FROM users WHERE id = ?", employee_id
            )

        # Log user in
        session.clear()
        session["user_id"] = user_id[0]["id"]
        session["first_name"] = user_id[0]["first_name"]

        # Redirect user to home page
        return redirect("/")

    # # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html", first_name=first_name)


# code taken from pset 9 - finance
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("employee_id"):
            return apology("must provide Employee ID", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", request.form.get("employee_id")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["first_name"] = rows[0]["first_name"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# taken from pset 9 - finance
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# adapted from pset 9 - finance
@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    first_name = session.get('first_name')
    if request.method == "POST":
        time = request.form.get("time")
        if time == 'week':
            #date format help from the duck
            history = db.execute(
                "SELECT user_id, id, register, date, time, variance FROM history WHERE strftime('%W', date) = strftime('%W', 'now') ORDER BY date DESC, time DESC"
            )

            var = db.execute(
                "SELECT SUM(variance) FROM history WHERE strftime('%W', date) = strftime('%W', 'now')"
            )
            # help from the duck to figure out how to pass the sum
            sum_variance=var[0]['SUM(variance)']

            return render_template("history.html", history=history, sum_variance=sum_variance, first_name=first_name)
        if time == 'month':
            #date format help from the duck
            history = db.execute(
                "SELECT user_id, id, register, date, time, variance FROM history WHERE strftime('%m', date) = strftime('%m', 'now') ORDER BY date DESC, time DESC"
            )

            var = db.execute(
                "SELECT SUM(variance) FROM history WHERE strftime('%m', date) = strftime('%m', 'now')"
            )
            # help from the duck to figure out how to pass the sum
            sum_variance=var[0]['SUM(variance)']

            return render_template("history.html", history=history, sum_variance=sum_variance, first_name=first_name)
        if time == 'year':
            #date format help from the duck
            history = db.execute(
                "SELECT user_id, id, register, date, time, variance FROM history WHERE strftime('%Y', date) = strftime('%Y', 'now') ORDER BY date DESC, time DESC"
            )

            var = db.execute(
                "SELECT SUM(variance) FROM history WHERE strftime('%Y', date) = strftime('%Y', 'now')"
            )
            # help from the duck to figure out how to pass the sum
            sum_variance=var[0]['SUM(variance)']

            return render_template("history.html", history=history, sum_variance=sum_variance, first_name=first_name)
    else:
        #date format help from the duck
        history = db.execute(
            "SELECT user_id, id, register, date, time, variance FROM history WHERE strftime('%W', date) = strftime('%W', 'now') ORDER BY date DESC, time DESC"
        )

        var = db.execute(
            "SELECT SUM(variance) FROM history WHERE strftime('%W', date) = strftime('%W', 'now')"
        )
        # help from the duck to figure out how to pass the sum
        sum_variance=var[0]['SUM(variance)']

        return render_template("history.html", history=history, sum_variance=sum_variance, first_name=first_name)

# adapted from pset 9 - finance
@app.route("/variances", methods=["GET", "POST"])
@login_required
def variances():
    first_name = session.get('first_name')

    if request.method == "POST":
        id = request.form.get("id")
        print("testing", id)
        time = request.form.get("time")
        if time == 'week':
            #date format help from the duck
            history = db.execute(
                "SELECT user_id, id, register, date, time, variance FROM history WHERE variance != 0 AND strftime('%W', date) = strftime('%W', 'now') ORDER BY date DESC, time DESC"
            )

            var = db.execute(
                "SELECT SUM(variance) FROM history WHERE variance != 0 AND strftime('%W', date) = strftime('%W', 'now')"
            )
            # help from the duck to figure out how to pass the sum
            sum_variance=var[0]['SUM(variance)']

            return render_template("variances.html", history=history, sum_variance=sum_variance, first_name=first_name)

        if time == 'month':
            #date format help from the duck
            history = db.execute(
                "SELECT user_id, id, register, date, time, variance FROM history WHERE variance != 0 AND strftime('%m', date) = strftime('%m', 'now') ORDER BY date DESC, time DESC"
            )

            var = db.execute(
                "SELECT SUM(variance) FROM history WHERE variance != 0 AND strftime('%m', date) = strftime('%m', 'now')"
            )
            # help from the duck to figure out how to pass the sum
            sum_variance=var[0]['SUM(variance)']

            return render_template("variances.html", history=history, sum_variance=sum_variance, first_name=first_name)
        if time == 'year':
            #date format help from the duck
            history = db.execute(
                "SELECT user_id, id, register, date, time, variance FROM history WHERE variance != 0 AND strftime('%Y', date) = strftime('%Y', 'now') ORDER BY date DESC, time DESC"
            )

            var = db.execute(
                "SELECT SUM(variance) FROM history WHERE variance != 0 AND strftime('%Y', date) = strftime('%Y', 'now')"
            )
            # help from the duck to figure out how to pass the sum
            sum_variance=var[0]['SUM(variance)']

            return render_template("variances.html", history=history, sum_variance=sum_variance, first_name=first_name)

    else:
        history = db.execute(
            "SELECT user_id, id, register, date, time, variance FROM history WHERE variance != 0 AND strftime('%W', date) = strftime('%W', 'now') ORDER BY date DESC, time DESC"
        )
        var = db.execute(
            "SELECT SUM(variance) FROM history WHERE strftime('%W', date) = strftime('%W', 'now')"
        )
        # help from the duck to figure out how to pass the sum
        sum_variance=var[0]['SUM(variance)']

        return render_template("variances.html", sum_variance=sum_variance, history=history, first_name=first_name)

@app.route("/count", methods=["GET", "POST"])
@login_required
def count():
    first_name = session.get('first_name')

    if request.method == "POST":
        if not request.form.get("register"):
            return apology("Must select register", 400)
        if not (request.form.get("hundred") and request.form.get("fifty") and request.form.get("twenty") and
                request.form.get("ten") and request.form.get("five") and request.form.get("one") and request.form.get("quarter")
                and request.form.get("dime") and request.form.get("nickel") and request.form.get("penny")):
            return apology("Must fill out all fields", 400)

        db.execute(
            "INSERT INTO history (user_id, date, time, register, hundred, fifty, twenty, ten, five, one, quarter, dime, nickel, penny, total, expected, variance) VALUES(?, CURRENT_DATE, CURRENT_TIME, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            session["user_id"], request.form.get("register"),
            request.form.get("hundred"), request.form.get("fifty"), request.form.get("twenty"),
            request.form.get("ten"), request.form.get("five"), request.form.get("one"),
            request.form.get("quarter"), request.form.get("dime"), request.form.get("nickel"), request.form.get("penny"),
            request.form.get("total"), request.form.get("expected"), request.form.get("variance")
        )

        history = db.execute(
            "SELECT user_id, id, register, date, time, variance FROM history WHERE strftime('%W', date) = strftime('%W', 'now') ORDER BY date DESC, time DESC"
        )
        var = db.execute(
            "SELECT SUM(variance) FROM history WHERE strftime('%W', date) = strftime('%W', 'now')"
        )
        sum_variance=var[0]['SUM(variance)']

        return render_template("history.html", first_name=first_name, sum_variance=sum_variance, history=history)

    else:
        return render_template("count.html", first_name=first_name)

@app.route("/view-count", methods=["GET"])
@login_required
def view_count():
    first_name = session.get('first_name')
    count_id = request.args.get('id')

    history = db.execute(
        "SELECT * FROM history WHERE id = ?", count_id
    )

    return render_template("view-count.html", first_name=first_name, history=history)

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, url_for
import requests
# For Python openweathermap
from pyowm.owm import OWM
# For Python datepicker
from datetime import date, timedelta
# For sending emails
import os
from flask_mail import Mail, Message
# For loading environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure application
app = Flask(__name__)

# Make sure secret key is set
if not os.environ.get("SECRET_KEY"):
    raise RuntimeError("SECRET_KEY not set")

app.secret_key = os.environ["SECRET_KEY"]

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure Mail variables
app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_PORT"] = 587
mail = Mail(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///bookings.db")

# Authenticated connection to Openweathermap API stored in owm object
owm = OWM(os.environ["OWM_TOKEN"])
mgr = owm.weather_manager()
weather = mgr.weather_at_coords(lat=37.9427787, lon=-0.7592459).weather.temperature ('celsius')
temp = round(weather['temp_max'])


@app.route("/")
def index():
    """Show Homepage"""

    # Uses Openweathermap
    return render_template("index.html", temp=temp)


@app.route("/photos")
def photos():
    """Show photos"""

    # Uses Bootstrap Carousel
    return render_template("photos.html")


@app.route("/tour")
def tour():
    """Show 360° tour"""

    return render_template("tour.html")


@app.route("/extras")
def extras():
    """Show optional extras"""

    # Ajax
    return render_template("extras.html")


@app.route("/transfers")
def transfers():

    return render_template("transfers.html")


@app.route("/beer")
def beer():

    return render_template("beer.html")


@app.route("/romance")
def romance():

    return render_template("romance.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact form"""

    # User reached route via POST (by submitting contact form)
    if request.method == "POST":
        bot = request.form.get("subject")
        name = request.form.get("name")
        email = request.form.get("email")
        content = request.form.get("message")

        # If subject was submitted (bot capcha) return to homepage
        if bot:
            return render_template("index.html")

        # Form validation server-side
        elif not name:
            flash("Must provide your name!")
            return render_template("contact.html")

        elif not email:
            flash("Must provide your email address " + name + "!")
            return render_template("contact.html")

        if not content:
            flash("Must provide a message" + name + "!")
            return render_template("contact.html")

        # Send me email with form data
        else:
            message = Message("CONTACT from " + name, recipients=["grahamcoyle@gmail.com"])
            message.body = "Message: " + content + "\r\n Email: " + email + "\r\n Name: " + name
            mail.send(message)
            return render_template("sent.html", name=name)

    # User reached route via GET (by clicking a link or via redirect)
    else:
        return render_template("contact.html")


@app.route("/sent")
def sent():
    """Confirmation message"""

    return render_template("sent.html")


@app.route("/golf")
def golf():

    return render_template("golf.html")


@app.route("/beach")
def beach():

    return render_template("beach.html")


@app.route("/shopping")
def shopping():

    return render_template("shopping.html")


@app.route("/karting")
def kartings():

    return render_template("karting.html")


@app.route("/book", methods=["GET", "POST"])
def book():
    """Booking enquiries"""


    # HOPEFULLY TO BE REPLACED WITH BOOKING FACILITY RATHER THAN JUST TAKING ENQUIRIES IN DUE COURSE
    # Set restictions for arrival and departure dates from between today until 1 year
    # change date format from default YYYY-MM-DD  to D MMM Y using strftime
    format = date.today()
    today = format.strftime("%d %b %Y")

    # Set initial endDate to 3 days from now (daterangepicker has no minimun range option)
    minbooking = format + timedelta(days=3)
    endDate = minbooking.strftime("%d %b %Y")

    # Set max date to 1 year from now (unless 29 Feb!)
    if format.month == 2 and format.day == 29:
        addyear = format.replace(year=format.year + 1, day=28)
    else:
        addyear = format.replace(year=format.year + 1)
    anniversary = addyear.strftime("%d %b %Y")

    # User reached route via POST (submitted form)
    if request.method == "POST":
        bot = request.form.get("subject")
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        verified = request.form.get("verified")
        arrival = request.form.get("arrival")
        departure = request.form.get("departure")

        # If hidden subject was filled (bot capcha) return to homepage
        if bot:
            return render_template("index.html")

        # Form validation server-side
        elif not name:
            flash("Must provide your name")
            return render_template("book.html", today=today, anniversary=anniversary, endDate=endDate)

        elif not email:
            flash("Must provide your email address " + name)
            return render_template("book.html", today=today, anniversary=anniversary, endDate=endDate)

        elif not arrival:
            flash("Must select arrival date " + name)
            return render_template("book.html", today=today, anniversary=anniversary, endDate=endDate)

        elif not departure:
            flash("Must select departure date " + name)
            return render_template("book.html", today=today, anniversary=anniversary, endDate=endDate)

        # Uses Twilio for phone verification
        elif phone and not verified:
            flash("Invalid phone number " + name)
            return render_template("book.html", today=today, anniversary=anniversary, endDate=endDate)

        elif phone and verified != "verified":
            flash("An error occurred " + name + ", please try again")
            flash(verified)
            return render_template("book.html", today=today, anniversary=anniversary, endDate=endDate)

        # Validated
        else:
            # Send me email with form data
            message = Message("RENTAL ENQUIRY from " + name, recipients=["grahamcoyle@gmail.com"])
            message.body = " Arrival: " + arrival + "\r\n Departure: " + departure + "\r\n Email: " + email + "\r\n Phone: " + phone
            mail.send(message)

            # Add booking enquiries to database
            db.execute("INSERT INTO enquiries (name, email, phone, arrival, departure) values(?, ?, ?, ?, ?)", name, email, phone, arrival, departure)
            return render_template("sent.html", name=name)

    # # User reached route via GET (by clicking a link or via redirect)
    else:
        return render_template("book.html", today=today, anniversary=anniversary, endDate=endDate)
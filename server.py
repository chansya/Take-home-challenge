"""Server for movie ratings app."""

from crypt import methods
from distutils.log import error
from zoneinfo import available_timezones
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, Reservation
from datetime import datetime, timedelta

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# dummy user 1= Sincere@april.biz
# dummy user 2= Shanna@melissa.tv


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("index.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")

    user = User.get_by_email(email)
    if not user:
        flash("The email you entered was incorrect.")
        return redirect("/")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
        return render_template("search.html")


@app.route("/search")
def view_search():
    return render_template("search.html")


@app.route("/search_res", methods=["POST"])
def search_reservations():
    """Search for available reservations."""

    user = User.get_by_email(session.get("user_email"))
    user_id = user.user_id

    # get the form input(date, start time & end time)
    input_date = datetime.strptime(request.form.get("res-date"),
                                   '%Y-%m-%d').date()
    start_time = datetime.strptime(request.form.get("start-time"),
                                   '%H:%M').time()
    end_time = datetime.strptime(request.form.get("end-time"),
                                 '%H:%M').time()

    # search if user has any reservation on that day
    error = None
    user_res = Reservation.query.filter(Reservation.user_id == user_id, 
                                        Reservation.date == input_date).first()

    # create error message if record is found on the same day
    if user_res:
        error = "You already have a booking on this day! Please book a tasting session on another day."

    # query database for existing reservations on the chosen day
    res_in_db = Reservation.query.filter(Reservation.date == input_date,
                                        Reservation.start_time >= start_time,
                                        Reservation.end_time <= end_time).all()

    exisitng_res = []
    for res in res_in_db:
        exisitng_res.append(res.start_time)

    # create avaible time slots for reservations
    available_times = []

    # create appointments for every time slot during the time period
    while start_time< end_time:
        current = start_time
        if current not in exisitng_res:
            # if the time is not booked, add into time_slots
            available_times.append(current)
        # add 30 min to the current time
        start_time = (datetime.combine(input_date, current)+ timedelta(minutes=30)).time()

    # render templates with available slots
    return render_template("booking.html", date=input_date, error=error, 
                            available_times=available_times, exisitng_res=exisitng_res)


@app.route("/create_res", methods=["POST"])
def make_reservation():
    """Create a new reservation"""
    user = User.get_by_email(session.get("user_email"))
    user_id = user.user_id

    res_date = datetime.strptime(request.form.get("chosen-date"),
                                   '%Y-%m-%d').date()

    start_time = datetime.strptime(request.form.get("chosen-time")[:5],
                                   '%H:%M').time()

    end_time= (datetime.combine(res_date, start_time)+ timedelta(minutes=30)).time()


    new_rec = Reservation.create(res_date, start_time, end_time, user_id)
    db.session.add(new_rec)
    db.session.commit()

    flash("Your booking was made successfully.")

    return render_template("search.html")


@app.route("/view_res")
def view_reservation():
    """Display user's reservation"""

    user = User.get_by_email(session.get("user_email"))
    user_id = user.user_id
    user_res = Reservation.query.filter(Reservation.user_id==user_id).all()

    return render_template("user_booking.html", user_res=user_res)

@app.route("/logout")
def process_logout():
    """Log user out and clear the session."""

    del session["user_email"]
    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

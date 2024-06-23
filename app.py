import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from sqlalchemy.exc import SQLAlchemyError
from helpers import login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///planner.db")


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
    user_id = session["user_id"]
    tasks_list = []
    unfinished_tasks = []
    # Retrieve tasks from the day table
    rows = db.execute(
        "SELECT name, date, tasks, task_status,id FROM day WHERE user_id = ?",
        user_id,
    )

    for row in rows:
        task = row["tasks"]
        task_status = row["task_status"]

        # Check if the task has the status 'unfinished'
        if task_status == "unfinished":
            tasks_list.append((task, row["name"], row["date"], row["id"]))
        else:
            unfinished_tasks.append((task, row["name"], row["date"], row["id"]))
    return render_template(
        "index.html", tasks_list=tasks_list, unfinished_tasks=unfinished_tasks
    )


@app.route("/delete_task", methods=["POST"])
@login_required
def delete_task():
    user_id = session["user_id"]
    task_id = request.form.get("task_id")

    # Perform the deletion of the task based on task_id and user_id
    db.execute("DELETE FROM day WHERE id = ? AND user_id = ?", task_id, user_id)

    flash("Task deleted successfully!")
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            error_message = "must provide username"
            return render_template("login.html", error_message=error_message)

        # Ensure password was submitted
        elif not request.form.get("password"):
            error_message = "must provide password"
            return render_template("login.html", error_message=error_message)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            error_message = "invalid username and/or password"
            return render_template("login.html", error_message=error_message)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    user_id = session["user_id"]
    now = datetime.datetime.now()
    today = now.strftime("%A")
    now_date = now.date()
    tasks_list = []
    choose_date = None  # Initialize choose_date
    day_name = today  # Default to the current day name
    error_message = None  # Initialize error_message

    if request.method == "POST":
        choose_date = request.form.get("choose_date")

        if not choose_date:
            error_message = "Please choose a date."

        else:
            # Convert the choose_date string to a datetime object
            chosen_date = datetime.datetime.strptime(choose_date, "%Y-%m-%d").date()
            # Update the day name for the selected date
            day_name = chosen_date.strftime("%A")

            # Fetch tasks for the chosen date
            rows = db.execute(
                "SELECT tasks, task_status FROM day WHERE user_id = ? AND date=?",
                user_id,
                chosen_date,
            )
            tasks_list = [(row["tasks"], row["task_status"]) for row in rows]

            selected_tasks = request.form.getlist(
                "tasks[]"
            )  # Use getlist instead of get
            if selected_tasks:
                db.execute(
                    "UPDATE day SET task_status = ? WHERE user_id = ? AND name = ? AND date = ? AND tasks IN (?)",
                    "finished",
                    user_id,
                    day_name,
                    chosen_date,
                    tuple(selected_tasks),
                )
                flash("Tasks marked as finished!")

            new_task = request.form.get("new_task")
            if not new_task:
                error_message = "Please enter task."
            else:
                db.execute(
                    "INSERT INTO day (user_id, name, tasks, task_status, date) VALUES (?, ?, ?, ?, ?)",
                    user_id,
                    day_name,
                    new_task,
                    "unfinished",
                    chosen_date,
                )
                flash("New task added!")

    # Fetch tasks for the chosen date or the default (current) date
    if not error_message:
        rows = db.execute(
            "SELECT tasks, task_status FROM day WHERE user_id = ? AND date=?",
            user_id,
            chosen_date if choose_date else now_date,
        )
        tasks_list = [(row["tasks"], row["task_status"]) for row in rows]

    return render_template(
        "add.html",
        today=today,
        tasks_list=tasks_list,
        date=chosen_date if choose_date else now_date,
        day_name=day_name,
        error_message=error_message,
    )


def get_today():
    now = datetime.datetime.now()
    return now.strftime("%A")


def is_password_strong(password):
    """Check if the password meets the complexity requirements."""
    return (
        any(c.isalpha() for c in password)
        and any(c.isdigit() for c in password)
        and any(c.isalnum() for c in password)
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Retrieve form data
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate form data
        if not username:
            error_message = "Must Give Username"
            return render_template("register.html", error_message=error_message)
        elif not password:
            error_message = "Must Give Password"
            return render_template("register.html", error_message=error_message)
        elif not confirmation:
            error_message = "Must Confirm Your Password"
            return render_template("register.html", error_message=error_message)
        elif confirmation != password:
            error_message = "Passwords Do Not Match"
            return render_template("register.html", error_message=error_message)
        # Check password complexity
        elif not is_password_strong(password):
            error_message = "Password must have letters, numbers, and/or symbols"
            return render_template("register.html", error_message=error_message)
        hash = generate_password_hash(password)

        try:
            # Insert new user into the database
            new_user = db.execute(
                "INSERT INTO users(username, hash) VALUES(?, ?)",
                username,
                hash,
            )
        except:
            error_message = "Username Already Exists"
            return render_template("register.html", error_message=error_message)

        session["user_id"] = new_user
        return redirect("/")

@app.route("/weekly")
@login_required
def weekly():
    user_id = session["user_id"]

    # Get the current week offset from the query parameters, default to 0 (current week)
    week_offset = int(request.args.get("week_offset", 0))

    # Calculate the start and end dates of the week based on the current date and week_offset
    now = datetime.datetime.now()
    start_of_week = now - datetime.timedelta(days=now.weekday()) + datetime.timedelta(weeks=week_offset)
    end_of_week = start_of_week + datetime.timedelta(days=6)

    # Retrieve tasks for the selected week
    rows = db.execute(
        "SELECT tasks, task_status, name FROM day WHERE user_id = ? AND date >= ? AND date <= ?",
        user_id, start_of_week.date(), end_of_week.date()
    )
    weekly_tasks = [(row["tasks"], row["task_status"], row["name"]) for row in rows]

    # Calculate the month and year for the header
    month_year = start_of_week.strftime("%B %Y")

    # Calculate the date for each day of the week
    days_week = [( (start_of_week + datetime.timedelta(days=i)).strftime("%A"), (start_of_week + datetime.timedelta(days=i)).date() ) for i in range(7)]

    return render_template(
        "weekly.html", weekly_tasks=weekly_tasks, days_week=days_week, week_offset=week_offset, month_year=month_year
    )



@app.route("/mark_done", methods=["POST"])
@login_required
def mark_done():
    user_id = session["user_id"]
    task_id = request.form.get("task_id")

    # Update the task status to "finished"
    db.execute(
        "UPDATE day SET task_status = ? WHERE id = ? AND user_id = ?",
        "finished",
        task_id,
        user_id,
    )

    flash("You have completed your task! 🙌")
    return redirect("/")


@app.route("/not_done", methods=["POST"])
@login_required
def not_done():
    user_id = session["user_id"]
    task_id = request.form.get("task_id")

    # Update the task status to "finished"
    db.execute(
        "UPDATE day SET task_status = ? WHERE id = ? AND user_id = ?",
        "unfinished",
        task_id,
        user_id,
    )

    flash("You didn't finish the task yet. Keep going!")
    return redirect("/")

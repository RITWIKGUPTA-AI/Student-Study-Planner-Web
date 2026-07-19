from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import os

from utils.auth import check_login
from utils.json_manager import read_json
from utils.helpers import get_current_date, get_current_time
from flask import request, render_template, redirect, url_for
from utils.json_manager import read_json, write_json

from routes.subjects import subjects_bp
from routes.tasks import tasks_bp
from routes.planner import planner_bp
from routes.notes import notes_bp
from routes.goals import goals_bp
from routes.attendance import attendance_bp
from flask import session, redirect, url_for
from routes.timetable import timetable_bp
from routes.analytics import analytics_bp
from routes.settings import settings_bp
from routes.reminders import reminders_bp
from routes.profile import profile_bp
from routes.achievements import achievements_bp
from routes.backup import backup_bp
from routes.search import search_bp
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
app = Flask(__name__)

# Secret key
app.secret_key = os.environ.get("SECRET_KEY", "studentplanner123")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Register Blueprints
app.register_blueprint(search_bp)
app.register_blueprint(subjects_bp)
app.register_blueprint(backup_bp)
app.register_blueprint(achievements_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(reminders_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(planner_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(goals_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(timetable_bp)
app.register_blueprint(analytics_bp)
@app.route("/dark-theme")
def dark_theme():

    session["theme"] = "dark"

    return redirect(request.referrer or url_for("dashboard"))


@app.route("/light-theme")
def light_theme():

    session["theme"] = "light"

    return redirect(request.referrer or url_for("dashboard"))
@app.route("/ai-quiz", methods=["GET", "POST"])
def ai_quiz():

    quiz = ""

    if request.method == "POST":

        topic = request.form["topic"]

        prompt = f"""
        Generate 10 multiple-choice questions for the topic: {topic}.

        For each question provide:
        - Question
        - 4 options (A, B, C, D)
        - Correct answer
        - Short explanation
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert exam question setter."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        quiz = response.choices[0].message.content

    return render_template(
        "ai_quiz.html",
        quiz=quiz
    )
@app.route("/ai-summarizer", methods=["GET", "POST"])
def ai_summarizer():

    summary = ""

    if request.method == "POST":

        notes = request.form["notes"]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize notes into short exam-ready bullet points."
                },
                {
                    "role": "user",
                    "content": notes
                }
            ]
        )

        summary = response.choices[0].message.content

    return render_template(
        "ai_summarizer.html",
        summary=summary
    )
@app.route("/ai-study-plan", methods=["GET", "POST"])
def ai_study_plan():

    plan = ""

    if request.method == "POST":

        subjects = request.form["subjects"]
        exam_date = request.form["exam_date"]
        study_hours = request.form["study_hours"]

        prompt = f"""
        Create a detailed study plan for a Class 11/12 student.

        Subjects: {subjects}
        Exam Date: {exam_date}
        Daily Study Hours: {study_hours}

        Make a day-wise timetable with revision and mock tests.
        Keep it practical and motivating.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert academic planner."},
                {"role": "user", "content": prompt}
            ]
        )

        plan = response.choices[0].message.content

    return render_template(
        "ai_study_plan.html",
        plan=plan
    )
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]


        users = read_json("students.json")


        # check duplicate username

        for user in users:

            if user.get("username") == username:

                flash("Username already exists")

                return redirect(
                    url_for("register")
                )


        new_user = {

            "name": name,
            "username": username,
            "password": password,
            "tasks": [],
            "notes": [],
            "goals": []

        }


        users.append(new_user)


        write_json(
            "students.json",
            users
        )


        flash("Account created successfully. Login now.")

        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )


# --------------------------------
# Login
# --------------------------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        print("---------- LOGIN DEBUG ----------")
        print("Entered username:", username)
        print("Entered password:", password)
        print("Users loaded:", users)
        print("--------------------------------")

        print("ENTERED USERNAME:", username)
        print("ENTERED PASSWORD:", password)

        users = read_json("students.json")

        print("USERS FROM FILE:", users)

        for user in users:

            print("CHECKING USER:", user)

            if (
                user.get("username") == username
                and user.get("password") == password
            ):

                print("LOGIN SUCCESS")

                session["username"] = username
                session["name"] = user.get("name")

                return redirect(url_for("dashboard"))


        print("LOGIN FAILED")
        flash("Invalid username or password")


    return str(users)
# --------------------------------
# Dashboard
# --------------------------------
@app.route("/dashboard")
def dashboard():

    from utils.json_manager import read_json
    from datetime import datetime

    subjects = read_json("subjects.json")
    tasks = read_json("tasks.json")
    notes = read_json("notes.json")
    goals = read_json("goals.json")
    reminders = read_json("reminders.json")
    timetable = read_json("timetable.json")
    attendance = read_json("attendance.json")
    planner = read_json("planner.json")
    profile = read_json("profile.json")

    today = datetime.now().strftime("%Y-%m-%d")

    # Today's reminders
    todays_reminders = []

    for reminder in reminders:
        if reminder.get("date") == today:
            todays_reminders.append(reminder)

    # Today's timetable
    day_name = datetime.now().strftime("%A")

    todays_classes = []

    for entry in timetable:
        if entry.get("day") == day_name:
            todays_classes.append(entry)

    # Attendance %

    total_classes = len(attendance)

    present = 0

    for item in attendance:
        if item.get("status") == "Present":
            present += 1

    attendance_percent = 0

    if total_classes > 0:
        attendance_percent = round((present / total_classes) * 100)

    completed_goals = 0

    for goal in goals:
        if goal.get("status") == "Completed":
            completed_goals += 1
    # Recent Tasks

    recent_tasks = tasks[-5:]

    # Recent Notes

    recent_notes = notes[-5:]
    quotes = [

        "Success is the sum of small efforts repeated every day.",

        "Discipline beats motivation.",

        "Dream big. Start small. Act now.",

        "Stay focused and never give up.",

        "Today's preparation is tomorrow's success.",

        "Consistency creates excellence.",

        "Every study session brings you closer to your goal."

    ]

    import random

    quote = random.choice(quotes)

    return render_template(

        "dashboard.html",

        current_date=get_current_date(),

        current_time=get_current_time(),
        quote=quote,

        study_hours=[2,3,4,5,6,4,3],

        study_days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],

        subjects=len(subjects),

        tasks=len(tasks),

        notes=len(notes),

        goals=len(goals),
        recent_tasks=recent_tasks,

        recent_notes=recent_notes,

        reminders=len(reminders),

        timetable=len(timetable),

        planner=len(planner),

        attendance=len(attendance),

        attendance_percent=attendance_percent,

        completed_goals=completed_goals,

        todays_reminders=todays_reminders,

        todays_classes=todays_classes,

        profile=profile

    )
# Logout
# --------------------------------
@app.route("/logout")
def logout():

    return redirect(url_for("login"))
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500
# -------------------------
# Error Pages
# -------------------------

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def internal_error(error):

    return render_template(
        "500.html"
    ), 500


# --------------------------------
# Run Application
# --------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
# Error Pages
# ===============================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "404.html"

    ), 404


@app.errorhandler(500)
def server_error(error):

    return render_template(

        "500.html"

    ), 500
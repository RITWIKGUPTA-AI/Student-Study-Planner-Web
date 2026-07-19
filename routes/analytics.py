from flask import Blueprint, render_template
from utils.json_manager import read_json
from flask import Blueprint, render_template, send_file
import csv
import os

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
def analytics():

    # ======================================
    # Read JSON Files
    # ======================================

    subjects = read_json("subjects.json")
    tasks = read_json("tasks.json")
    notes = read_json("notes.json")
    goals = read_json("goals.json")
    planner = read_json("planner.json")
    attendance = read_json("attendance.json")
    reminders = read_json("reminders.json")
    timetable = read_json("timetable.json")

    # ======================================
    # Task Statistics
    # ======================================

    completed_tasks = 0

    pending_tasks = 0

    high_priority = 0

    medium_priority = 0

    low_priority = 0

    for task in tasks:

        if isinstance(task, dict):

            if task.get("status") == "Completed":

                completed_tasks += 1

            else:

                pending_tasks += 1

            if task.get("priority") == "High":

                high_priority += 1

            elif task.get("priority") == "Medium":

                medium_priority += 1

            elif task.get("priority") == "Low":

                low_priority += 1

    if len(tasks) > 0:

        task_progress = round(

            completed_tasks * 100 / len(tasks),

            2

        )

    else:

        task_progress = 0

    # ======================================
    # Goal Statistics
    # ======================================

    completed_goals = 0

    pending_goals = 0

    for goal in goals:

        if isinstance(goal, dict):

            if goal.get("status") == "Completed":

                completed_goals += 1

            else:

                pending_goals += 1

    if len(goals) > 0:

        goal_progress = round(

            completed_goals * 100 / len(goals),

            2

        )

    else:

        goal_progress = 0

    # ======================================
    # Attendance
    # ======================================

    present = 0

    absent = 0

    for item in attendance:

        if isinstance(item, dict):

            if item.get("status") == "Present":

                present += 1

            else:

                absent += 1

    if len(attendance) > 0:

        attendance_percentage = round(

            present * 100 / len(attendance),

            2

        )

    else:

        attendance_percentage = 0

    # ======================================
    # Planner Statistics
    # ======================================

    total_minutes = 0

    for plan in planner:

        if isinstance(plan, dict):

            try:

                total_minutes += int(

                    plan.get("duration", 0)

                )

            except:

                pass

    total_hours = round(

        total_minutes / 60,

        2

    )

    # ======================================
    # Weekly Study Data
    # ======================================

    weekly_data = [

        2,

        3,

        4,

        5,

        3,

        6,

        4

    ]

    # ======================================
    # Monthly Study Data
    # ======================================

    monthly_data = [

        25,

        30,

        28,

        32,

        35,

        40

    ]

    # ======================================
    # Subject Distribution
    # ======================================

    subject_labels = []

    subject_values = []

    for subject in subjects:

        if isinstance(subject, dict):

            subject_labels.append(

                subject.get(

                    "name",

                    "Subject"

                )

            )

            subject_values.append(1)

        else:

            subject_labels.append(str(subject))

            subject_values.append(1)

    # ======================================
    # Render Template
    # ======================================

    return render_template(

        "analytics.html",

        subject_count=len(subjects),

        task_count=len(tasks),

        note_count=len(notes),

        goal_count=len(goals),

        planner_count=len(planner),

        reminder_count=len(reminders),

        timetable_count=len(timetable),

        attendance_count=len(attendance),

        completed_tasks=completed_tasks,

        pending_tasks=pending_tasks,

        completed_goals=completed_goals,

        pending_goals=pending_goals,

        task_progress=task_progress,

        goal_progress=goal_progress,

        attendance_percentage=attendance_percentage,

        present=present,

        absent=absent,

        total_minutes=total_minutes,

        total_hours=total_hours,

        high_priority=high_priority,

        medium_priority=medium_priority,

        low_priority=low_priority,

        weekly_data=weekly_data,

        monthly_data=monthly_data,

        subject_labels=subject_labels,

        subject_values=subject_values

    )
@analytics_bp.route("/analytics/export/csv")
def export_csv():

    filename = "analytics_report.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(["Category", "Value"])

        writer.writerow(["Subjects", len(read_json("subjects.json"))])

        writer.writerow(["Tasks", len(read_json("tasks.json"))])

        writer.writerow(["Notes", len(read_json("notes.json"))])

        writer.writerow(["Goals", len(read_json("goals.json"))])

        writer.writerow(["Planner", len(read_json("planner.json"))])

        writer.writerow(["Attendance", len(read_json("attendance.json"))])

        writer.writerow(["Reminders", len(read_json("reminders.json"))])

        writer.writerow(["Timetable", len(read_json("timetable.json"))])

    return send_file(

        filename,

        as_attachment=True

    )
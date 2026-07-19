from flask import Blueprint, render_template, request, redirect, url_for
from utils.json_manager import read_json, write_json

achievements_bp = Blueprint("achievements", __name__)


@achievements_bp.route("/achievements", methods=["GET", "POST"])
def achievements():

    achievements = read_json("achievements.json")

    if request.method == "POST":

        achievement = {
            "title": request.form["title"],
            "description": request.form["description"],
            "date": request.form["date"]
        }

        achievements.append(achievement)

        write_json("achievements.json", achievements)

        return redirect(url_for("achievements.achievements"))

    return render_template(
        "achievements.html",
        achievements=achievements
    )


@achievements_bp.route("/achievements/delete/<int:index>")
def delete_achievement(index):

    achievements = read_json("achievements.json")

    if 0 <= index < len(achievements):

        achievements.pop(index)

        write_json("achievements.json", achievements)

    return redirect(url_for("achievements.achievements"))
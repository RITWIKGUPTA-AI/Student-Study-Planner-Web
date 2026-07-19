from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.json_manager import read_json, write_json

settings_bp = Blueprint("settings", __name__)


DEFAULT_SETTINGS = {

    "theme": "Light",

    "notifications": "On",

    "font_size": "Medium",

    "language": "English"

}


@settings_bp.route("/settings", methods=["GET", "POST"])
def settings():

    settings = read_json("settings.json")

    if not settings:

        settings = DEFAULT_SETTINGS.copy()

        write_json("settings.json", settings)

    if request.method == "POST":

        # Reset Button

        if request.form.get("action") == "reset":

            write_json("settings.json", DEFAULT_SETTINGS)

            flash(

                "Settings reset successfully!",

                "success"

            )

            return redirect(url_for("settings.settings"))

        # Save Settings

        settings["theme"] = request.form.get(
            "theme",
            "Light"
        )

        settings["notifications"] = request.form.get(
            "notifications",
            "On"
        )

        settings["font_size"] = request.form.get(
            "font_size",
            "Medium"
        )

        language = request.form.get(
            "language",
            "English"
        ).strip()

        if language == "":

            language = "English"

        settings["language"] = language

        write_json("settings.json", settings)

        flash(

            "Settings saved successfully!",

            "success"

        )

        return redirect(url_for("settings.settings"))

    return render_template(

        "settings.html",

        settings=settings

    )
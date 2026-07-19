from flask import Blueprint, render_template, send_file, flash, redirect, url_for
import os
import shutil
from datetime import datetime
from flask import request
import zipfile

backup_bp = Blueprint("backup", __name__)

DATA_FOLDER = "data"
BACKUP_FOLDER = "backups"


@backup_bp.route("/backup")
def backup():

    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_name = f"StudentPlanner_Backup_{timestamp}"

    zip_path = shutil.make_archive(

        os.path.join(BACKUP_FOLDER, backup_name),

        "zip",

        DATA_FOLDER

    )

    flash(

        "Backup created successfully!",

        "success"

    )

    return send_file(

        zip_path,

        as_attachment=True

    )


@backup_bp.route("/backup_page")
def backup_page():

    backups = []

    if os.path.exists(BACKUP_FOLDER):

        backups = sorted(

            os.listdir(BACKUP_FOLDER),

            reverse=True

        )

    return render_template(

        "backup.html",

        backups=backups

    )


@backup_bp.route("/backup/download/<filename>")
def download_backup(filename):

    return send_file(

        os.path.join(BACKUP_FOLDER, filename),

        as_attachment=True

    )


@backup_bp.route("/backup/delete/<filename>")
def delete_backup(filename):

    file_path = os.path.join(

        BACKUP_FOLDER,

        filename

    )

    if os.path.exists(file_path):

        os.remove(file_path)

        flash(

            "Backup deleted successfully!",

            "success"

        )

    return redirect(

        url_for("backup.backup_page")

    )
@backup_bp.route("/backup/restore", methods=["POST"])
def restore_backup():

    if "backup_file" not in request.files:

        flash(

            "Please select a backup file.",

            "danger"

        )

        return redirect(url_for("backup.backup_page"))

    file = request.files["backup_file"]

    if file.filename == "":

        flash(

            "No file selected.",

            "danger"

        )

        return redirect(url_for("backup.backup_page"))

    if not file.filename.endswith(".zip"):

        flash(

            "Please upload a ZIP backup.",

            "danger"

        )

        return redirect(url_for("backup.backup_page"))

    temp_zip = os.path.join(

        BACKUP_FOLDER,

        "temp_restore.zip"

    )

    file.save(temp_zip)

    try:

        with zipfile.ZipFile(temp_zip, "r") as zip_ref:

            zip_ref.extractall(DATA_FOLDER)

        os.remove(temp_zip)

        flash(

            "Backup restored successfully!",

            "success"

        )

    except Exception:

        flash(

            "Invalid backup file.",

            "danger"

        )

    return redirect(url_for("backup.backup_page"))
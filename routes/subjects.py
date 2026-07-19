from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.json_manager import read_json, write_json

subjects_bp = Blueprint("subjects", __name__)


@subjects_bp.route("/subjects", methods=["GET", "POST"])
def subjects():

    subjects = read_json("subjects.json")

    if request.method == "POST":

        new_subject = request.form.get("subject", "").strip()

        # -------------------------
        # Validation
        # -------------------------

        if new_subject == "":

            flash(
                "Subject name cannot be empty!",
                "danger"
            )

            return redirect(url_for("subjects.subjects"))

        # Duplicate validation (case-insensitive)
        for subject in subjects:

            if subject.lower() == new_subject.lower():

                flash(
                    "Subject already exists!",
                    "warning"
                )

                return redirect(url_for("subjects.subjects"))

        # -------------------------
        # Save Subject
        # -------------------------

        subjects.append(new_subject)

        write_json("subjects.json", subjects)

        flash(
            "Subject added successfully!",
            "success"
        )

        return redirect(url_for("subjects.subjects"))

    # -------------------------
    # Search
    # -------------------------

    search = request.args.get("search", "").lower().strip()

    if search:

        filtered = []

        for subject in subjects:

            if search in subject.lower():

                filtered.append(subject)

    else:

        filtered = subjects

    return render_template(
        "subjects.html",
        subjects=filtered,
        total=len(subjects)
    )


@subjects_bp.route("/delete_subject/<subject>")
def delete_subject(subject):

    subjects = read_json("subjects.json")

    if subject in subjects:

        subjects.remove(subject)

        write_json("subjects.json", subjects)

        flash(
            "Subject deleted successfully!",
            "success"
        )

    else:

        flash(
            "Subject not found!",
            "danger"
        )

    return redirect(url_for("subjects.subjects"))


@subjects_bp.route("/edit_subject/<old_name>", methods=["GET", "POST"])
def edit_subject(old_name):

    subjects = read_json("subjects.json")

    if request.method == "POST":

        new_name = request.form.get("subject", "").strip()

        # -------------------------
        # Validation
        # -------------------------

        if new_name == "":

            flash(
                "Subject name cannot be empty!",
                "danger"
            )

            return redirect(
                url_for(
                    "subjects.edit_subject",
                    old_name=old_name
                )
            )

        # Duplicate validation
        for subject in subjects:

            if (
                subject.lower() == new_name.lower()
                and subject.lower() != old_name.lower()
            ):

                flash(
                    "Another subject with this name already exists!",
                    "warning"
                )

                return redirect(
                    url_for(
                        "subjects.edit_subject",
                        old_name=old_name
                    )
                )

        # -------------------------
        # Update Subject
        # -------------------------

        updated = False

        for i in range(len(subjects)):

            if subjects[i] == old_name:

                subjects[i] = new_name

                updated = True

                break

        if updated:

            write_json("subjects.json", subjects)

            flash(
                "Subject updated successfully!",
                "success"
            )

        else:

            flash(
                "Subject not found!",
                "danger"
            )

        return redirect(url_for("subjects.subjects"))

    return render_template(
        "edit_subject.html",
        old_name=old_name
    )
import json
import os

DATA_FOLDER = "data"


def read_json(filename):

    filepath = os.path.join(DATA_FOLDER, filename)

    if not os.path.exists(filepath):

        return []

    try:

        with open(filepath, "r", encoding="utf-8") as file:

            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):

        return []

    except Exception:

        return []


def write_json(filename, data):

    filepath = os.path.join(DATA_FOLDER, filename)

    try:

        with open(filepath, "w", encoding="utf-8") as file:

            json.dump(
                data,
                file,
                indent=4
            )

    except Exception as error:

        print(error)
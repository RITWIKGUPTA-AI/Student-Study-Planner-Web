from utils.json_manager import read_json

def check_login(username, password):

    login_data = read_json("login.json")

    # If login.json contains a single object
    if isinstance(login_data, dict):
        return (
            login_data.get("username") == username
            and login_data.get("password") == password
        )

    # If login.json contains a list of users
    if isinstance(login_data, list):
        for user in login_data:
            if (
                user.get("username") == username
                and user.get("password") == password
            ):
                return True

    return False
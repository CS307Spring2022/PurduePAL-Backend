from typing import Tuple

from helpers import check_password, db, check_for_data


def login(data: dict) -> Tuple[bool, str, str]:
    if not check_for_data(data, "email", "password"):
        return False, "", "",True,True
    email = data["email"]
    password = data["password"]
    email_exists = db["users"].find_one(filter={"$or": [{"_id": email}, {"username": email}]})

    if email_exists:
        hashed_pass = email_exists["password"]
        if check_password(password, hashed_pass):
            return True, email_exists["_id"], email_exists["username"],email_exists["public"],email_exists["darkMode"]
        else:
            # wrong password entered
            return False, "", "",True,True
    else:
        # email doesnt exist
        return False, "", "",True,True

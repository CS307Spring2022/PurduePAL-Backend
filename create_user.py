from helpers import safeget, db


def sign_up(data: dict) -> bool:
    first_name = safeget(data, "first_name")
    if not first_name:
        return False
    last_name = safeget(data, "last_name")
    if not last_name:
        return False
    email = safeget(data, "email")
    if not email:
        return False
    username = safeget(data, "username")
    if not username:
        return False
    password = safeget(data, "password")
    if not password:
        return False


def add_bio_to_user(data: dict) -> bool:
    email = safeget(data, "email")
    if not email:
        return False
    bio = safeget(data, "bio")
    if not bio:
        return False
    if len(bio) > 160:
        return False
    stat = db["users"].update_one(filter={"_id": email}, update={"$set": {"bio": bio}})  # update user with email
    if stat.matched_count == 0:
        return False
    return True
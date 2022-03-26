from helpers import safeget, db, check_for_data


def getUserInfo(data: dict) -> dict:
    if not check_for_data(data, "email"):
        return {}
    email = safeget(data, "email")
    info = db["users"].find_one({"_id": email})
    print(type(info))
    return info


def sign_up(data: dict) -> bool:
    if not check_for_data(data, "first_name", "last_name", "email", "username", "password"):
        return False
    first_name = safeget(data, "first_name")
    last_name = safeget(data, "last_name")
    email = safeget(data, "email")
    username = safeget(data, "username")
    password = safeget(data, "password")


def add_bio_to_user(data: dict, update_db: bool = True) -> bool:
    if not check_for_data(data, "email", "bio"):
        return False
    email = safeget(data, "email")
    bio = safeget(data, "bio")
    first_name = safeget(data, "firstName")
    last_name = safeget(data, "lastName")
    if len(bio) > 160:
        return False

    if update_db:
        stat = db["users"].update_one(filter={"_id": email}, update={"$set": {"bio": bio, "firstName": first_name, "lastName": last_name}})  # update user with email
        if stat.matched_count == 0:
            return False
    return True

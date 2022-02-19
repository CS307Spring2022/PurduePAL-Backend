from helpers import safeget


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


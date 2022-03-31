from helpers import check_for_data, db, generate_confirmation_code, send_email


def delete_post_from_db(data: dict, live: bool = True) -> bool:
    if not check_for_data(data, "email", "post_id"):
        return False
    email = data["email"]
    post_id = data["post_id"]
    if live:
        status = db["posts"].delete_one(filter={"_id": post_id, "poster": email})
        if status.deleted_count != 1:
            return False
        return True


def delete_user_with_conf_code(data: dict, live: bool = True) -> bool:
    if not check_for_data(data, "email", "confirmation_code"):
        return False
    email = data["email"]
    conf_code = data["confirmation_code"]
    if live:
        status = db["users"].delete_one(filter={"_id": email, "confirmation_code": conf_code})
        if status.deleted_count != 1:
            return False
        status = db["posts"].delete_many(filter={"poster": email})
        if not status.acknowledged:
            return False
        return True


def delete_user_without_conf_code(data: dict, live: bool = True) -> bool:
    if not check_for_data(data, "email"):
        return False
    email = data["email"]
    if live:
        confirmation_code_generated = str(generate_confirmation_code())
        status = db["users"].update_one(filter={"_id": email},
                                        update={"$set": {"confirmation_code": confirmation_code_generated}})
        send_email(to_email=email,
                   text=f"0.0.0.0:5000/delete_user?confirmation_code={confirmation_code_generated}&email={email}",
                   subject="Confirmation Code")
        if status.modified_count != 1:
            return False
        return True

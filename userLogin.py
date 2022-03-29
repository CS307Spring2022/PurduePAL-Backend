from typing import Tuple
from helpers import check_password, safeget, db, check_for_data
from error import Errors


def login(data: dict) -> Tuple[bool, str, str]:
	if not check_for_data(data, "email", "password"):
		return False, "", ""
	email = data["email"]
	password = data["password"]
	email_exists = db["users"].find_one(filter={"$or": [{"_id": email}, {"username": email}]})

	if email_exists:
		hashed_pass = email_exists["password"]
		if check_password(password, hashed_pass):
			return True, email_exists["_id"], email_exists["username"]
		else:
			#wrong password entered
			return False, "", ""
	else:
		#email doesnt exist
		return False, "", ""
		
	



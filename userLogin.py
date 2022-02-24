from helpers import check_password, safeget, db, check_for_data
from error import Errors


def login(data:dict, email: str, given_pass: str) ->bool:
	email_exists = db["users"].find_one(filter={"_id": email})

	if email_exists:
		email_value = email_exists["email"]
		hashed_pass = email_exists["password"]
		if check_password(hashed_pass, given_pass):
			return True
		else:
			#wrong password entered
			return Errors.PASSWORD_ERROR
	else:
		#email doesnt exist
		return Errors.EMAIL_ERROR
		
	



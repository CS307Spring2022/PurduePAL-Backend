import os
import smtplib
import ssl
from random import randint

import certifi
import pymongo
from passlib.context import CryptContext

db = pymongo.MongoClient(os.getenv("CONN"), tlsCAFile=certifi.where())["PurduePAL"]
smtp_server = os.getenv("SMTP_SERVER")
port = os.getenv("PORT")
sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("PASSWORD")
context = ssl.create_default_context()  # to send email

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


def safeget(obj, *keys, default=None):
    """Retrieve values from nested keys in a dict safely.
    :param _dict: The dict containing the desired keys and values.
    :type _dict: dict
    :param *keys: The key structure in the dict leading to the desired value.
    :type *keys: iterable of str or int. Must be a str for dictionary, must be int for array.
    :param default: The default value if the key is not in the dictionary, or index is out of bounds for the array.
    :type default: any
    :returns: The value of the nested keys in the dict, default if any key does not exist.
    :rtype: any
    """

    val = obj
    for key in keys:
        try:
            val = val[key]
        except:
            return default
    if val is None:
        return default
    return val


def check_for_data(data: dict, *keys) -> bool:
    for key in keys:
        exist = safeget(data, key)
        if not exist:
            return False
    return True


def encrypt_password(user_password: str) -> str:
    return pwd_context.hash(user_password)


def check_password(entered_password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(entered_password, hashed)
    except ValueError:
        return False
    except TypeError:
        return False


def generate_confirmation_code() -> int:
    range_start = 10 ** (5 - 1)
    range_end = (10 ** 5) - 1
    return randint(range_start, range_end)


def send_email(subject: str, text: str, to_email: str) -> bool:
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            net_text = f"""\
            Subject: {subject}
   
            {text}"""
            server.sendmail(sender_email, to_email, net_text)
            return True
    except Exception as e:
        print(e)
        return False


def verifyConfirmation(to_email: str):
    conf_code = generate_confirmation_code
    subject = "Purdue PAL: Verify Confirmation for Account Creation"
    content = "Please click the following link to verify your account: " + conf_code

    send_email(subject, content, to_email)

    # check that user is not already active
    # check if link has been clicked

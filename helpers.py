import os

import pymongo
from passlib.context import CryptContext
db = pymongo.MongoClient(os.getenv("CONN"))["PurduePAL"]

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


def encrypt_password(password: str) -> str:
    return pwd_context.hash(password)


def check_password(password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(password, hashed)
    except ValueError:
        return False
    except TypeError:
        return False
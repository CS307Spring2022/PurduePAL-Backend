import os
import unittest

import helpers
from create_user import add_bio_to_user
from helpers import encrypt_password, check_password
from userVerification import checkUsername, unique_user


class SignUpTests(unittest.TestCase):
    def test_encrypt(self):
        encrypted = encrypt_password("password")
        self.assertNotEqual(encrypted, "password")  # did it encrypt?
        decrypted = check_password("password", encrypted)
        self.assertTrue(decrypted)   # can it decrypt normally?
        decrypted = check_password("passw0rd", encrypted)
        self.assertFalse(decrypted)  # what if user input is wrong?
        encrypted = encrypted[:-1] + '!'
        decrypted = check_password("password", encrypted)
        self.assertFalse(decrypted)  # what if encrypted is wrong?

    def test_username(self):
        in_use = unique_user("anonymous")  # username for anonymous, even with incomplete profile
        self.assertNotEqual(in_use, True)
        in_use = unique_user("justinhart")  # complete profile. does it work?
        self.assertNotEqual(in_use, True)
        newUsername = helpers.generate_confirmation_code()
        in_use = unique_user(str(newUsername))  # absolutely new username (99% unique)
        self.assertEqual(in_use, True)


class ProfileTest(unittest.TestCase):
    def test_add_bio(self):
        user_data = {
            "email": "purduepete@gmail.com",
            "bio": "hehe"
        }
        added = add_bio_to_user(user_data, update_db=False)
        self.assertTrue(added)
        added = add_bio_to_user(user_data.pop("email"), update_db=False)
        self.assertFalse(added)
        user_data = {
            "email": "purduepete@gmail.com",
            "bio": "hehe"
        }
        added = add_bio_to_user(user_data.pop("bio"), update_db=False)
        self.assertFalse(added)


if __name__ == '__main__':
    unittest.main()

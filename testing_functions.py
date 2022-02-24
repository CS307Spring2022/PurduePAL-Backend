import unittest

from create_user import add_bio_to_user
from helpers import encrypt_password, check_password


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


class DeleteUserStuff(unittest.TestCase):
    def test_delete_post(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

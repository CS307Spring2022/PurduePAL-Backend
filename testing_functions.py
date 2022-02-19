import unittest

from helpers import encrypt_password, check_password


class SignUpTests(unittest.TestCase):
    def test_encrypt(self):
        encrypted = encrypt_password("password")
        self.assertNotEqual(encrypted, "password")  # did it encrypt?
        decrypted = check_password("password", encrypted)
        self.assertEqual(decrypted, True)   # can it decrypt normally?
        decrypted = check_password("passw0rd", encrypted)
        self.assertEqual(decrypted, False)  # what if user input is wrong?
        encrypted = encrypted[:-1] + '!'
        decrypted = check_password("password", encrypted)
        self.assertEqual(decrypted, False)  # what if encrypted is wrong?


if __name__ == '__main__':
    unittest.main()

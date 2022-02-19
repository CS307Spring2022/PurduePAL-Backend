import unittest

from helpers import encrypt_password, check_password


class SignUpTests(unittest.TestCase):
    def test_encrypt(self):
        encrypted = encrypt_password("password")
        self.assertNotEqual(encrypted, "password")  # add assertion here
        decrypted = check_password("password", encrypted)
        self.assertEqual(decrypted, True)
        decrypted = check_password("passw0rd", encrypted)
        self.assertEqual(decrypted, False)
        encrypted = encrypted[:-1] + '!'
        decrypted = check_password("password", encrypted)
        self.assertEqual(decrypted, False)


if __name__ == '__main__':
    unittest.main()

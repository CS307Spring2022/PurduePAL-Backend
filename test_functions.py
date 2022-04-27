import unittest

import helpers
from create_user import add_bio_to_user, sign_up
from follow import user1_follow_user2, user1_unfollow_user2, user_follow_topic, user_unfollow_topic
from helpers import encrypt_password, check_password
from userLogin import login
from userVerification import unique_user


class SignUpTests(unittest.TestCase):
    def test_encrypt(self):
        encrypted = encrypt_password("password")
        self.assertNotEqual(encrypted, "password")  # did it encrypt?
        decrypted = check_password("password", encrypted)
        self.assertTrue(decrypted)  # can it decrypt normally?
        decrypted = check_password("passw0rd", encrypted)
        self.assertFalse(decrypted)  # what if user input is wrong?
        encrypted = encrypted[:-1] + '!'
        decrypted = check_password("password", encrypted)
        self.assertFalse(decrypted)  # what if encrypted is wrong?

    def test_username(self):
        in_use = unique_user("anonymous")  # username for anonymous, even with incomplete profile
        self.assertNotEqual(in_use, True)
        in_use = unique_user("")  # bad username profile. does it work?
        self.assertNotEqual(in_use, True)
        newUsername = helpers.generate_confirmation_code()
        in_use = unique_user(str(newUsername))  # absolutely new username (99% unique)
        self.assertEqual(in_use, True)

    def test_sign_up(self):
        user_data = {
            "firstName": str(helpers.generate_confirmation_code()),  # new
            "lastName": str(helpers.generate_confirmation_code()),  # new
            "email": "anonymous@purdue.edu",  # already used
            "username": str(helpers.generate_confirmation_code()),  # new
            "password": "hellowhyamihere",  # long enough
            "confirmPassword": "hellowhyamihere"  # long enough
        }
        status, signed_up = sign_up(user_data, testing=True)
        self.assertNotEqual(status, 200)
        user_data["email"] = str(helpers.generate_confirmation_code()) + "@purdue.edu"
        status, signed_up = sign_up(user_data, testing=True)
        self.assertEqual(status, 200)

    def test_login(self):
        login_data = {
            "email": "anonymous@purdue.edu",
            "password": ""
        }
        yay, email, username, _, _ = login(login_data)
        self.assertFalse(yay)
        login_data["password"] = "lol"
        yay, email, username, _, _ = login(login_data)
        self.assertTrue(yay)
        self.assertEqual("anonymous@purdue.edu", email)
        self.assertEqual("anonymous", username)


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

    def test_change_name(self):
        user_data = {
            "email": "anonymous@purdue.edu",
            "bio": "hehe",
            "firstName": "Anonymous",
            "lastName": "Anonymous"
        }
        edited = add_bio_to_user(user_data)
        self.assertTrue(edited)
        user = helpers.db["users"].find_one({"_id": "anonymous@purdue.edu"})
        self.assertEqual(user["bio"], "hehe")
        self.assertEqual(user["firstName"], 'Anonymous')
        self.assertEqual(user["lastName"], 'Anonymous')


class UserActions(unittest.TestCase):
    user1id = "anonymous@purdue.edu"

    def test_follow_user(self):
        user1id = self.user1id
        user2id = "rajeshr@purdue.edu"
        ret = user1_follow_user2(user1id, user2id)
        self.assertTrue(ret)
        ret = user1_follow_user2(user1id, user1id[:-1])
        self.assertFalse(ret)
        ret = user1_follow_user2(user1id, user2id)
        self.assertFalse(ret)
        self.assertTrue(user2id in helpers.db["users"].find_one(user1id)["usersFollowing"])

    def test_unfollow_user(self):
        user1id = self.user1id
        user2id = "rajeshr@purdue.edu"
        ret = user1_unfollow_user2(user1id, user2id)
        self.assertTrue(ret)
        ret = user1_unfollow_user2(user1id, user2id)
        self.assertFalse(ret)
        self.assertFalse(user2id in helpers.db["users"].find_one(user1id)["usersFollowing"])

    topic_id = "topic6"

    def test_follow_topic(self):
        data = {
            "email": self.user1id,
            "topic": self.topic_id
        }
        ret, _ = user_follow_topic(data)
        self.assertTrue(ret)
        ret, _ = user_follow_topic(data)
        self.assertFalse(ret)
        self.assertTrue(self.topic_id in helpers.db["users"].find_one(self.user1id)["topicsFollowing"])

    def test_unfollow_topic(self):
        data = {
            "email": self.user1id,
            "topic": self.topic_id
        }
        ret, _ = user_unfollow_topic(data)
        self.assertTrue(ret)
        ret, _ = user_unfollow_topic(data)
        self.assertFalse(ret)
        self.assertFalse(self.topic_id in helpers.db["users"].find_one(self.user1id)["topicsFollowing"])


if __name__ == '__main__':
    unittest.main()

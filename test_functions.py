import unittest
from collections import defaultdict

import helpers
from create_post import reactPost
from create_user import add_bio_to_user, sign_up, update_public, getUserInfo
from follow import user1_follow_user2, user1_unfollow_user2, user_follow_topic, user_unfollow_topic
from helpers import encrypt_password, check_password
from timeline import get_timeline
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
        login_data["password"] = "Anonymous123!"
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

    def testPrivatePublic(self):
        data = {
            "email": "anonymous@purdue.edu",
            "public": False
        }
        update_public(data)
        self.assertTrue(helpers.db["users"].find_one({"_id": data["email"]})["public"])
        data["public"] = True
        update_public(data)
        self.assertFalse(helpers.db["users"].find_one({"_id": data["email"]})["public"])


class PostTests(unittest.TestCase):
    def testCommentTopicName(self):
        comment = helpers.db["posts"].find_one({"parentID": {"$ne": None}})
        parent = helpers.db["posts"].find_one({"_id": comment["parentID"]})
        self.assertEqual(parent["topic"], comment["topic"])

    data = {"email": "alice93@purdue.edu"}

    def testTimelineExists(self):
        timeline, ret = get_timeline(self.data)
        self.assertTrue(ret)
        self.timeline = timeline

    def testTimelineTopicFollow(self):
        self.timeline, ret = get_timeline(self.data)
        user = helpers.db["users"].find_one({"_id": self.data["email"]})
        for post in self.timeline:
            for topic in user["topicsFollowing"]:
                if post["topic"] == topic:
                    return
        self.fail("Couldn't find a post in the timeline from a topic you follow.")

    def testTimelineUserFollow(self):
        self.timeline, ret = get_timeline(self.data)
        user = helpers.db["users"].find_one({"_id": self.data["email"]})
        # print(user["usersFollowing"])
        for post in self.timeline:
            for user in user["usersFollowing"]:
                # print(user, post["user"]["email"])
                if post["user"]["email"] == user:
                    return
        self.fail("Couldn't find a post in the timeline from a person you follow.")

    def testProfileViewLoggedOut(self):
        data = defaultdict()
        data["profileUser"] = "raj123"
        self.assertNotEqual(getUserInfo(data), {})

    def testProfileViewLoggedIn(self):
        data = defaultdict()
        data["profileUser"] = "raj123"
        data["loggedUser"] = "raj123"
        self.assertNotEqual(getUserInfo(data), {})

    def testTimelineChronologicalSort(self):
        timeline, ret = get_timeline(self.data)
        for i in range(1, len(timeline)):
            if timeline[i]["timestamp"] < timeline[i - 1]["timestamp"]:  # backend is reversed
                self.fail("Timeline is out of order")


class UserlineTests(unittest.TestCase):
    def testUserlineChronologicalSort(self):
        data = defaultdict()
        data["profileUser"] = "raj123"
        data["loggedUser"] = "raj123"
        timeline = getUserInfo(data)
        print(timeline)
        timeline = timeline["createdPostsObject"]
        for i in range(1, len(timeline)):
            if timeline[i]["timestamp"] > timeline[i - 1]["timestamp"]:  # backend is reversed
                self.fail("Timeline is out of order")

    def testPrivateUserline(self):
        data = {"profileUser": "anonymous"}
        userline = getUserInfo(data)
        if userline["public"]:
            self.fail("Private account viewable")

    def testUserlineInteractionsChronologicalSort(self):
        data = defaultdict()
        data["profileUser"] = "raj123"
        data["loggedUser"] = "raj123"
        timeline = getUserInfo(data)
        print(timeline)
        timeline = timeline["interactedPostsObject"]
        for i in range(1, len(timeline)):
            if timeline[i]["timestamp"] > timeline[i - 1]["timestamp"]:  # backend is reversed
                self.fail("Timeline is out of order")

    def testPrivateUserlineInteractions(self):
        data = {"profileUser": "anonymous"}
        userline = getUserInfo(data)
        if userline["public"]:
            self.fail("Private account viewable")


class CommentReactions(unittest.TestCase):
    data = {
        "postID": "626602df0e6e0e5e43f5b343",
        "email": "anonymous@purdue.edu"
    }

    def testLikeComment(self):
        self.data["interaction"] = 1
        self.assertTrue(reactPost(self.data))

    def testDisLikeComment(self):
        self.data["interaction"] = 2
        self.assertTrue(reactPost(self.data))

    def testUnlikeComment(self):
        self.data["interaction"] = 3
        self.assertTrue(reactPost(self.data))

    def testunDisLikeComment(self):
        self.data["interaction"] = 4
        self.assertTrue(reactPost(self.data))


if __name__ == '__main__':
    unittest.main()

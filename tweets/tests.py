from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestTweets(APITestCase):

    URL = "http://127.0.0.1:8000/api/v1/tweets/"
    PAYLOAD_TEST = "PAYLOAD TEST 1"
    PAYLOAD_TEST_2 = "PAYLOAD TEST 2"

    def test_tweets(self):
        response = self.client.get(self.URL)
        # 빈 리스트 return
        self.assertIsInstance(
            response.data, list, "test_tweets: 데이터가 리스트가 아닙니다"
        )
        # status 200
        self.assertEqual(
            response.status_code, 200, "test_tweets: 코드가 200이 아닙니다."
        )
        # login 없이 post
        response = self.client.post(self.URL)
        self.assertEqual(
            response.status_code, 403, "test_tweets: 코드가 403이 아닙니다."
        )

        user = User.objects.create(
            username="test_tweets",
        )
        user.set_password("123")
        user.save()
        self.client.force_login(
            user,
        )
        # login 후 payload 없이 post
        response = self.client.post(self.URL)
        self.assertEqual(
            response.status_code, 400, "test_tweets: 코드가 400이 아닙니다."
        )
        response = self.client.get(self.URL)
        self.assertEqual(
            len(response.data), 0, "test_tweets: 데이터의 개수가 0이 아닙니다"
        )
        response = self.client.post(
            self.URL,
            data={"payload": self.PAYLOAD_TEST},
        )
        self.assertEqual(
            response.status_code, 200, "test_tweets: post 성공시 코드가 200이 아닙니다."
        )
        self.assertEqual(
            response.data.get("payload"),
            self.PAYLOAD_TEST,
            "test_tweets - post: payload 값이 잘못됐습니다.",
        )
        response = self.client.get(self.URL)
        self.assertEqual(
            response.status_code, 200, "test_tweets: get 성공시 코드가 200이 아닙니다."
        )
        self.assertEqual(
            response.data[0].get("payload"),
            self.PAYLOAD_TEST,
            "test_tweets - get: payload 값이 잘못됐습니다.",
        )
        self.assertEqual(
            len(response.data), 1, "test_tweets: 데이터의 개수가 1이 아닙니다"
        )
        response = self.client.post(
            self.URL,
            data={"payload": self.PAYLOAD_TEST_2},
        )
        response = self.client.get(self.URL)
        self.assertEqual(
            response.status_code, 200, "test_tweets: get 성공시 코드가 200이 아닙니다."
        )
        self.assertEqual(
            response.data[1].get("payload"),
            self.PAYLOAD_TEST_2,
            "test_tweets - get: payload 값이 잘못됐습니다.",
        )
        self.assertEqual(
            len(response.data), 2, "test_tweets: 데이터의 개수가 2이 아닙니다"
        )


class TestTweetDetail(APITestCase):

    URL = "http://127.0.0.1:8000/api/v1/tweets/"
    PAYLOAD_1 = "tweet detail test 1"
    PAYLOAD_2 = "tweet detail test 2"

    def setUp(self):
        # user 생성
        # tweet 1개 생성
        user = User.objects.create(username="user_other")
        user.set_password("123")
        user.save()
        self.user_other = user
        user = User.objects.create(username="user_tweet")
        user.set_password("123")
        user.save()
        self.client.force_login(
            user,
        )
        self.client.post(self.URL, {"payload": "tweet detail test id 1"})
        self.client.post(self.URL, {"payload": self.PAYLOAD_2})

    def test_tweet_detail(self):
        # get test
        # 없는 id url
        response = self.client.get(f"{self.URL}10")
        self.assertEqual(response.status_code, 404, "TweetDetail: 404 필요")
        # 있는 id url
        url = f"{self.URL}1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, "TweetDetail: 200 필요")

        # put test login - 제대로 된 user - 값 제대로
        response = self.client.put(url, {"payload": self.PAYLOAD_1})
        self.assertEqual(response.status_code, 200, "TweetDetail: 200 필요")
        self.assertEqual(
            response.data.get("payload"), self.PAYLOAD_1, "TweetDetail: put 작동 이상"
        )

        # put test login - 제대로 된 user - 값 이상하게
        response = self.client.put(url, {})
        self.assertEqual(response.status_code, 400, "TweetDetail: 400 필요")

        # delete test login - 제대로 된 user
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, "TweetDetail: 204 필요")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404, "TweetDetail: 404 필요")

        url = f"{self.URL}2"
        self.client.logout()

        # put test login 없이
        response = self.client.put(url, {"payload": self.PAYLOAD_1})
        self.assertEqual(response.status_code, 403, "TweetDetail put: 403 - login 필요")
        self.assertNotEqual(response.data.get("payload"), self.PAYLOAD_1)

        # delete test login 없이
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, 403, "TweetDetail delete: 403 - login 필요"
        )
        response = self.client.get(url)
        self.assertEqual(response.data.get("payload"), self.PAYLOAD_2)

        self.client.force_login(self.user_other)

        # put test login - 다른 user
        response = self.client.put(url, {"payload": self.PAYLOAD_1})
        self.assertEqual(response.status_code, 403, "TweetDetail put: 403, user 불일치")
        self.assertNotEqual(response.data.get("payload"), self.PAYLOAD_1)

        # delete test login - 다른 user
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, 403, "TweetDetail delete: 403, user 불일치"
        )
        response = self.client.get(url)
        self.assertEqual(response.data.get("payload"), self.PAYLOAD_2)

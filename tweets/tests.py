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

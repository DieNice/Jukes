from django.test import TestCase
from django.contrib.auth.models import User
from .models import Follower


class UsersTestCase(TestCase):
    def test_simple(self):
        self.assertEqual(1 + 1, 2, 'Hard test')

    def test_request_list_users(self):
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)

    def test_unknown_url(self):
        response = self.client.get('/v1/user12312/')
        self.assertEqual(response.status_code, 404)

    def test_empty_list_users(self):
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        })

    def test_list_users(self):
        User.objects.create(username="JackKelly")
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [{
                "email": "",
                "first_name": "",
                "last_name": "",
                "url": "http://testserver/v1/users/JackKelly/",
                "username": "JackKelly"
            }]
        })


class FollowerTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(username="Kelvin")
        self.user2 = User.objects.create(username="Garry")
        self.user3 = User.objects.create(username="Tormund")
        Follower.objects.create(follower=self.user1, follows=self.user2)

    def test_data_exists(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(Follower.objects.count(), 1)

    def test_new_follower_correct(self):
        self.client.force_login(self.user1)
        response = self.client.post('/v1/follow/Tormund/')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Follower.objects.count(), 2)
        self.assertIsNotNone(Follower.objects.filter(
            follower=self.user1, follows=self.user3
        ))

    def test_new_follower_correct(self):
        self.client.force_login(self.user1)
        response = self.client.delete('/v1/follow/Garry/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Follower.objects.count(), 0)

    def test_follow_yourself_faild(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user1}/')
        self.assertEqual(response.status_code, 400)

    def test_unfollow_not_exists_faild(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/NotExists/')
        self.assertEqual(response.status_code, 400)

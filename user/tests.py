from django.test import TestCase

# Create your tests here.

# ys

from .models import Profile, User


def test_user_search(self):

        Profile.objects.create(user=self.user)

        user2 = User.objects._create_user(
            name="tester", password="tester123", email="adefemi@yahoo.com")
        Profile.objects.create(user=user2)

        user3 = User.objects._create_user(
            name="vasman", password="vasman123", email="adefemi@yahoo.com2")
        Profile.objects.create(user=user3)

        # test keyword = adefemi oseni 
        url = self.profile_url + "?keyword=adefemi oseni"

        response = self.client.get(url, **self.bearer)
        result = response.json()["results"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 0)

        # test keyword = ade
        url = self.profile_url + "?keyword=ade"

        response = self.client.get(url, **self.bearer)
        result = response.json()["results"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]["user"]["name"], "vasman")
        self.assertEqual(result[1]["message_count"], 0)
        
        
        # test keyword = vester
        url = self.profile_url + "?keyword=vester"

        response = self.client.get(url, **self.bearer)
        result = response.json()["results"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["user"]["username"], "tester")
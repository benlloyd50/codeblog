from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.exceptions import ErrorDetail
from rest_framework import status

from snippets.models import BannedUser
from snippets.permissions import IsNotBanned


class SnippetTestCase(TestCase):
    def setUp(self) -> None:
        """Setups for making requests
        Will also authenticate the client with the username `ben`
        """
        self.client = APIClient()

        User = get_user_model()
        user = User.objects.create(username="ben", password="123")
        self.client.force_authenticate(user=user)

    def test_create_success(self):
        response = self.client.post(
            "/snippets/",
            r"""{
                "title": "code 4",
                "code": "int x = 20;\n",
                "linenos": false,
                "language": "java",
                "style": "friendly"
            }""",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_fake_language(self):
        """Tests the endpoint correctly checks the language as an invalid choice"""
        response = self.client.post(
            "/snippets/",
            r"""{
                "title": "code 4",
                "code": "int x = 20;\n",
                "linenos": false,
                "language": "fake",
                "style": "friendly"
            }""",
            content_type="application/json",
        )

        self.assertEqual(
            response.content, b'{"language":["\\"fake\\" is not a valid choice."]}'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fake_style(self):
        """Tests the endpoint correctly checks the style as an invalid choice"""
        response = self.client.post(
            "/snippets/",
            r"""{
                "title": "code 4",
                "code": "int x = 20;\n",
                "linenos": false,
                "language": "python",
                "style": "fake"
            }""",
            content_type="application/json",
        )

        self.assertEqual(
            response.content, b'{"style":["\\"fake\\" is not a valid choice."]}'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BannedUserTestCase(TestCase):
    def setUp(self) -> None:
        """Setups a banned user named `neb` and initializes client"""
        self.client = APIClient()

    def test_banned_user_cannot_post(self):
        """Tests a banned user cannot create a snippet"""
        username = "neb"
        password = "123"
        user = create_banned_user(username, password)
        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/snippets/",
            r"""{
                "title": "code 4",
                "code": "int x = 20;\n",
                "linenos": false,
                "language": "python",
                "style": "fake"
            }""",
            content_type="application/json",
        )
        self.assertJSONEqual(
            response.content,
            {"detail": ErrorDetail(string=IsNotBanned.message)},
        )

    def test_squashed_ban_can_post(self):
        """Test a user who has a SQUASHED ban (unbanned) can create a snippet"""
        username = "neb"
        password = "123"
        user = create_squashed_ban_user(username, password)
        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/snippets/",
            r"""{
                "title": "code 4",
                "code": "int x = 20;\n",
                "linenos": false,
                "language": "python",
                "style": "friendly"
            }""",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


def create_banned_user(username, password):
    User = get_user_model()
    user = User.objects.create_user(username=username, password=password)
    ban = BannedUser.objects.create(user_id=user, status="BANNED")
    ban.save()
    return user


def create_squashed_ban_user(username, password):
    User = get_user_model()
    user = User.objects.create_user(username=username, password=password)
    ban = BannedUser.objects.create(user_id=user, status="SQUASHED")
    ban.save()
    return user


def get_bearer_token(client: APIClient, username, password):
    """Requests a token from the API and adds the token into the headers"""
    bearer_resp = client.post(
        "/api/token/", data={"username": username, "password": password}
    )
    access_token = bearer_resp.data["access"]
    client.credentials(HTTP_AUTHORIZATION="Token " + access_token)

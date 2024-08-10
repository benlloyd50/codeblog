from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class SnippetTestCase(TestCase):
    def setUp(self) -> None:
        """Setups for making requests
        Will also authenticate the client with the username `ben`
        """
        self.client = APIClient()
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

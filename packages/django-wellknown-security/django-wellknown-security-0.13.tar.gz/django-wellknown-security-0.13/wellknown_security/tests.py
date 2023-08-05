from http import HTTPStatus

from django.conf import settings
from django.test import TestCase


class SecurityTxtTests(TestCase):
    def test_get(self):
        response = self.client.get("/.well-known/security.txt")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["content-type"], "text/plain")
        content = response.content.decode()
        self.assertTrue(content.startswith("Contact: "))

    def test_post_disallowed(self):
        response = self.client.post("/.well-known/security.txt")

        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, response.status_code)

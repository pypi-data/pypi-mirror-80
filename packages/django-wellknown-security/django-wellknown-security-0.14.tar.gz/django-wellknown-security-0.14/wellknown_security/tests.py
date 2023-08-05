# -*- coding: utf-8 -*-
__author__ = "Peter Gastinger"
__copyright__ = "Copyright 2020"
__credits__ = ["Peter Gastinger"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Peter Gastinger"
__email__ = "peter@secitec.net"
__status__ = "Production"

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

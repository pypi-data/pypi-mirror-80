#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the auth session decorator."""
from unittest.mock import patch
from unittest import TestCase
from cherrypy import HTTPRedirect
from pacifica.auth import auth_session


class AuthSessionTest(TestCase):
    """Test the auth_session method."""

    @patch('cherrypy.request')
    def test_happy(self, cp_request):
        """Test the happy path."""
        setattr(cp_request, 'user', 'Something True')

        @auth_session
        def wrapped(_self):
            return '1234'
        self.assertEqual(wrapped(self), '1234', 'If CherryPy user is set should act normally')

    def test_error(self):
        """Test the error exception path."""
        @auth_session
        def wrapped(_self):
            return 'not getting here'
        with self.assertRaises(HTTPRedirect):
            wrapped(self)

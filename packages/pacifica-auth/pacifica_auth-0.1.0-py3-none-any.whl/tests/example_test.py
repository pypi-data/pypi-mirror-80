#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the example module."""
from os import getenv, unlink
from os.path import isfile
import argparse
import cherrypy
from cherrypy.test import helper
import requests
from pacifica.auth import auth_session, pacifica_auth_arguments, error_page_default, social_settings
from pacifica.auth.user_model import User, Base
from pacifica.auth.root import Root


# pylint: disable=too-few-public-methods
class HelloWorld:
    """Example cherrypy hello world app."""

    exposed = True

    @cherrypy.tools.json_out()
    @auth_session
    # pylint: disable=no-self-use
    # pylint: disable=invalid-name
    def GET(self, error=None):
        """Example get method."""
        if error:
            raise cherrypy.HTTPError(500, error)
        return {'message': 'Hello World!'}


class TestExampleAuth(helper.CPWebCase):
    """Test the example class."""

    PORT = 8080
    HOST = '127.0.0.1'
    url = 'http://{0}:{1}'.format(HOST, PORT)

    @classmethod
    def setup_server(cls):
        """Setup the server configs."""
        _parser = argparse.ArgumentParser(description='testing command line')
        pacifica_auth_arguments(_parser)
        cls._args = _parser.parse_args([
            '--social-setting=github_key={}'.format(getenv('PA_TESTING_GITHUB_KEY', '')),
            '--social-setting=github_secret={}'.format(getenv('PA_TESTING_GITHUB_SECRET', ''))
        ])
        social_settings(cls._args, User, 'pacifica.auth.user_model.User')
        cherrypy.config.update({
            'server.socket_host': cls.HOST,
            'server.socket_port': cls.PORT
        })
        cherrypy.tree.mount(HelloWorld(), '/hello', config={
            '/': {
                'error_page.default': error_page_default,
                'request.dispatch': cherrypy.dispatch.MethodDispatcher()
            }
        })
        cherrypy.tree.mount(Root(cls._args.sa_module, cls._args.app_dir), '/', config={'/': {}})

    def setUp(self) -> None:
        """Setup the test by creating database schema."""
        Base.metadata.create_all(self._args.engine)
        # this needs to be imported after cherrypy settings are applied.
        # pylint: disable=import-outside-toplevel
        from social_cherrypy.models import SocialBase
        SocialBase.metadata.create_all(self._args.engine)

    def tearDown(self) -> None:
        """Tear down the test by deleting the database."""
        if isfile('database.sqlite3'):
            unlink('database.sqlite3')

    def test_main(self):
        """Test the add method in example class."""
        resp = requests.get('{}/hello'.format(self.url), allow_redirects=False)
        self.assertEqual(resp.status_code, 303)
        self.assertEqual(resp.headers['Location'], '{}/'.format(self.url))
        resp = requests.get(resp.headers['Location'], allow_redirects=False)
        self.assertEqual(resp.status_code, 303)
        self.assertEqual(resp.headers['Location'], '{}/login/github'.format(self.url))
        resp = requests.get(resp.headers['Location'], allow_redirects=False)
        self.assertEqual(resp.status_code, 303)
        self.assertTrue('https://github.com/login/oauth/authorize' in resp.headers['Location'])

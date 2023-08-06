#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Base application module."""
from os import makedirs
from os.path import isdir, join, dirname
import json
import importlib
import cherrypy
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import create_engine
from .satool import SATool
from .saplugin import SAEnginePlugin


def error_page_default(**kwargs):
    """Error page when something goes wrong."""
    cherrypy.response.headers['Content-Type'] = 'application/json'
    return bytes(json.dumps(kwargs), 'utf-8')


def session_commit():
    """Commit the user session to the database."""
    # pylint: disable=no-member
    cherrypy.session.save()


def check_sa_module_class(args):
    """Check the combination of module and class."""
    try:
        sa_module = importlib.import_module('social_core.backends.{}'.format(args.sa_module))
    except ImportError as ex:
        raise ValueError('Module {} is not a social core backend'.format(args.sa_module)) from ex
    if not getattr(sa_module, args.sa_class, None):
        raise ValueError('Social core backend module {} has no class {}'.format(args.sa_module, args.sa_class))


def check_sa_settings(obj_str):
    """Verify social auth settings."""
    if '=' not in obj_str:
        raise ValueError('{} must contain the "=" character'.format(obj_str))
    parts = obj_str.split('=')
    return 'SOCIAL_AUTH_{}'.format(parts[0].upper()), parts[1]


def pacifica_auth_arguments(parser):
    """Add Pacifica authentication command line arguments."""
    parser.add_argument(
        '--session-dir', dest='session_dir', default='sessions',
        help='Sesion directory for writing'
    )
    parser.add_argument(
        '--db-url', dest='engine', type=create_engine, default='sqlite:///database.sqlite3',
        help='Database url to connect to'
    )
    parser.add_argument(
        '--social-module', dest='sa_module', type=str,
        default='github', help='Social Core backend module name'
    )
    parser.add_argument(
        '--social-class', dest='sa_class', type=str, default='GithubOAuth2',
        help='Social Core backend auth class'
    )
    parser.add_argument(
        '--social-setting', dest='sa_settings', type=check_sa_settings,
        help='Social Core settings', action='append', default=[]
    )
    parser.add_argument(
        '--app-dir', dest='app_dir', type=str, default='app',
        help='ReactJS App directory to serve'
    )


def social_settings(args, user_class, user_import_path):
    """Setup the social settings for pacifica auth."""
    def load_user():
        """Load the user into the request."""
        # pylint: disable=no-member
        user_id = cherrypy.session.get('user_id')
        if user_id:
            cherrypy.request.user = cherrypy.request.db.query(user_class).get(user_id)
        else:
            cherrypy.request.user = None
    cherrypy.config.update({
        'SOCIAL_AUTH_USER_MODEL': user_import_path,
        'SOCIAL_AUTH_LOGIN_URL': '/login',
        'SOCIAL_AUTH_LOGIN_REDIRECT_URL': '/',
        'SOCIAL_AUTH_TRAILING_SLASH': True,
        'SOCIAL_AUTH_AUTHENTICATION_BACKENDS': (
            'social_core.backends.{}.{}'.format(args.sa_module, args.sa_class),
        )
    })
    for key, value in args.sa_settings:
        cherrypy.config.update({key: value})
    check_sa_module_class(args)
    SAEnginePlugin(cherrypy.engine, args.engine.url).subscribe()
    if not isdir(args.session_dir):
        makedirs(args.session_dir)
    cherrypy.config.update({
        'tools.sessions.on': True,
        'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
        'tools.sessions.storage_path': args.session_dir,
        'tools.sessions.timeout': 60,
        'tools.db.on': True,
        'tools.authenticate.on': True,
    })
    cherrypy.tools.jinja2env = Environment(
        loader=FileSystemLoader(join(dirname(__file__), 'templates'))
    )
    cherrypy.tools.db = SATool()
    cherrypy.tools.authenticate = cherrypy.Tool('before_handler', load_user)
    cherrypy.tools.session = cherrypy.Tool('on_end_resource', session_commit)

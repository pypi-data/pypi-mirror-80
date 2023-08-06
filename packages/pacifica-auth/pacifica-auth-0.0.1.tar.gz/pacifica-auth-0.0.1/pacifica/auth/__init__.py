#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Pacifica Authentication Module."""
import functools
import cherrypy
from .application import pacifica_auth_arguments, error_page_default, social_settings


def auth_session(func):
    """Authenticate the method."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        """Internal wrapper method."""
        if not getattr(cherrypy.request, 'user', None):
            raise cherrypy.HTTPRedirect('/')
        return func(self, *args, **kwargs)
    return wrapper


__all__ = [
    'auth_session',
    'pacifica_auth_arguments',
    'error_page_default',
    'social_settings'
]

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Root class to handle social auth."""
from os.path import join
import cherrypy
from cherrypy.lib.static import serve_file
from social_cherrypy.views import CherryPyPSAViews


class Root(CherryPyPSAViews):
    """Root class to integrate social auth."""

    def __init__(self, sa_module, app_dir):
        """Save the sa module and app directory."""
        self.sa_module = sa_module
        self.app_dir = app_dir

    @cherrypy.expose
    def index(self):
        """If the user isn't there redirect to login."""
        if not getattr(cherrypy.request, 'user', None):
            raise cherrypy.HTTPRedirect('/login/{}'.format(self.sa_module))
        raise cherrypy.HTTPRedirect('/app')

    @cherrypy.expose
    def app(self, *args):
        """Serve the app or redirect to login."""
        if not args:
            return serve_file(join(self.app_dir, 'index.html'))
        args = list(args)
        page = args.pop(0)
        if not (page in ['manifest.json'] or getattr(cherrypy.request, 'user', None)):
            raise cherrypy.HTTPRedirect('/login/{}'.format(self.sa_module))
        return serve_file(join(self.app_dir, page, *args))

    @cherrypy.expose
    # pylint: disable=no-self-use
    def done(self):
        """Done with the social auth login."""
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    # pylint: disable=no-self-use
    def logout(self):
        """Logout the user deleting the session."""
        if not getattr(cherrypy.request, 'user', None):
            raise cherrypy.HTTPRedirect('/')
        # pylint: disable=no-member
        cherrypy.session.clear()
        raise cherrypy.HTTPRedirect('/')


__all__ = ['Root']

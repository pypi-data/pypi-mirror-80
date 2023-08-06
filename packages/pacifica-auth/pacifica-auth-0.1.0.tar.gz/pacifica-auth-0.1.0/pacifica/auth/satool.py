#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Social Auth Tools to setup database connections."""
import cherrypy


class SATool(cherrypy.Tool):
    """CherryPy tool to manage handler."""

    def __init__(self):
        """Create the SATool and set bind priority."""
        super().__init__(
            'before_handler',
            self.bind_session,
            priority=20
        )

    def _setup(self):
        """Setup and attach the hooks."""
        super()._setup()
        cherrypy.request.hooks.attach(
            'on_end_resource',
            self.commit_transaction,
            priority=80
        )

    # pylint: disable=no-self-use
    def bind_session(self):
        """Bind the db session to something we can use."""
        session = cherrypy.engine.publish('bind-session').pop()
        cherrypy.request.db = session

    # pylint: disable=no-self-use
    def commit_transaction(self):
        """Delete the db session and publish commit."""
        if not hasattr(cherrypy.request, 'db'):
            return
        cherrypy.request.db = None
        cherrypy.engine.publish('commit-session')

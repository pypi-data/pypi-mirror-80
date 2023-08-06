#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy plugin to manage SQLAlchemy session connection."""
from cherrypy.process import plugins
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class SAEnginePlugin(plugins.SimplePlugin):
    """CherryPy SQLAlchemy Plugin."""

    def __init__(self, bus, connection_string=None):
        """Create the plugin saving engine connection and session."""
        self.sa_engine = None
        self.connection_string = connection_string
        self.session = scoped_session(sessionmaker(autoflush=True,
                                                   autocommit=False))
        super().__init__(bus)

    def start(self):
        """Start the engine connection and subscribe bind and commit."""
        self.sa_engine = create_engine(self.connection_string, echo=False)
        self.bus.subscribe('bind-session', self.bind)
        self.bus.subscribe('commit-session', self.commit)

    def stop(self):
        """Unsubscribe bind and commit and dispose of engine."""
        self.bus.unsubscribe('bind-session', self.bind)
        self.bus.unsubscribe('commit-session', self.commit)
        if self.sa_engine:
            self.sa_engine.dispose()
            self.sa_engine = None

    def bind(self):
        """Bind the session to the engine."""
        self.session.configure(bind=self.sa_engine)
        return self.session

    def commit(self):
        """Commit the session to the database or rollback."""
        # pylint: disable=no-member
        try:
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise Exception from ex
        finally:
            self.session.remove()

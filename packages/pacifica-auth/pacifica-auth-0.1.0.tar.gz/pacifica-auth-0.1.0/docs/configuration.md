# Configuration

The configuration of Pacifica Authentication is done on the command
line using arguments passed to services that incorporate the library.

## Authentication Options

These are common command line switches when Pacifica services include
the authentication library.

### Session Directory `--session-dir`

Default is `sessions` and contains the user sessions managed by the
core service.

### Database URL `--db-url`

Default is `sqlite:///database.sqlite3` and is the SQLAlchemy engine
[connection url](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls)

### Social Auth Module `--social-module`

Python Social Auth
[backends](https://python-social-auth.readthedocs.io/en/latest/backends/)
Python module name. The module name is relative to `social_core.backends`.

### Social Auth Class `--social-class`

Python Social Auth class name from the module in the `--social-module`
name.

### Social Auth Settings `--social-setting`

Python Social Auth
[settings](https://python-social-auth.readthedocs.io/en/latest/configuration/settings.html)
are passed as to CherryPy configrations. Examples are the following:

```
pacifica-service \
  --social-setting=github_key=<GitHub OAuth Key> \
  --social-setting=github_secret=<GitHub OAuth Secret>
```

### Application Directory `--app-dir`

This is optional as some Pacifica services don't serve applications
to users. This can serve both ReactJS or Swagger-UI as example
applications.

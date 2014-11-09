Jetee-tools
===========

Jetee tools is utility that provides range of `config resolvers` which are to help your app get connected with Jetee
services.

Installation
============

Install from PyPI::

    pip install jetee-tools

Or install the in-development version::

    pip install -e git+https://github.com/WhackoJacko/Jetee.git#egg=jetee


Usage example
=============

Basic usage example::

    from redis import Redis
    from jetee_tools.service_resolvers import JeteeServiceConfigResolver

    #instantiate config resolver with service hostname
    config_resolver = JeteeServiceConfigResolver(host=u'my-project-redis')

    #once config resolver instantiated, you can access service`s ip and port
    redis_connection = Redis(host=config_resolver.ip, port=config_resolver.port)

In order to be convenient in usage Jetee tools provides specific config resolvers with implemented ``render`` method::

    from jetee_tools.service_resolvers import DjangoDatabaseJeteeServiceConfigResolver

    #Django database settings
    DATABASES = {
        'default': DjangoDatabaseJeteeServiceConfigResolver(
            host=u'my-project-postgresql',
            protocol=u'postgresql_psycopg2'
        ).render()
    }

This equivalent to::

    DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': u'docker',
                'USER': u'docker',
                'PASSWORD': 'docker',
                'HOST': '172.17.42.1',
                'PORT': 49166,
            },
    }

See the API reference for more config resolvers.

.. toctree::
jetee_tools
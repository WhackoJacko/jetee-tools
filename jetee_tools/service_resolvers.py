import DNS


class JeteeServiceConfigResolver(object):
    dns_server = '172.17.42.1'
    service_ip = u'172.17.42.1'
    protocol = u''

    def get_real_host(self):
        return u'{}.service.consul'.format(self.host)

    def __init__(self, host):
        self.host = host

    def render(self, port):
        raise NotImplementedError

    def resolve(self):
        port = None
        srv_req = DNS.Request(qtype='srv', server=self.dns_server)
        srv_result = srv_req.req(self.host)
        for result in srv_result.answers:
            if result['typename'] == 'SRV':
                port = result[u'data'][2]
        assert port is not None
        return self.render(port)


class DjangoDatabaseJeteeServiceConfigResolver(JeteeServiceConfigResolver):
    def __init__(self, host, protocol):
        self.protocol = protocol
        self.host = host

    def render(self, port):
        return {
            'ENGINE': 'django.db.backends.{}'.format(self.protocol),
            # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'docker',  # Or path to database file if using sqlite3.
            'USER': 'docker',  # Not used with sqlite3.
            'PASSWORD': u'docker',  # Not used with sqlite3.
            'HOST': self.host,  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': port,  # Set to empty string for default. Not used with sqlite3.
        }


class RedisJeteeServiceConfigResolver(JeteeServiceConfigResolver):
    protocol = u'redis'

    def __init__(self, host, db=0):
        self.db = db
        self.host = host

    def render(self, port):
        return u'redis://{}:{}/{}'.format(self.service_ip, port, self.db)
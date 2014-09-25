import DNS


class JeteeServiceConfigResolver(object):
    dns_server = '172.17.42.1'
    service_ip = u'172.17.42.1'
    protocol = u''
    port = None

    def get_real_host(self):
        return u'{}.service.consul'.format(self.host)

    def __init__(self, host):
        self.host = host
        self.resolve_port()

    def as_string(self):
        raise NotImplementedError

    def resolve_port(self):
        port = None
        srv_req = DNS.Request(qtype='srv', server=self.dns_server)
        srv_result = srv_req.req(self.get_real_host())
        for result in srv_result.answers:
            if result['typename'] == 'SRV':
                port = result[u'data'][2]
        self.port = port


class DjangoDatabaseJeteeServiceConfigResolver(JeteeServiceConfigResolver):
    def __init__(self, host, protocol):
        self.protocol = protocol
        self.host = host
        self.resolve_port()

    def as_string(self):
        return {
            'ENGINE': 'django.db.backends.{}'.format(self.protocol),
            # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'docker',  # Or path to database file if using sqlite3.
            'USER': 'docker',  # Not used with sqlite3.
            'PASSWORD': u'docker',  # Not used with sqlite3.
            'HOST': self.service_ip,  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': self.port,  # Set to empty string for default. Not used with sqlite3.
        }


class RedisJeteeServiceConfigResolver(JeteeServiceConfigResolver):
    protocol = u'redis'

    def __init__(self, host, db=0):
        self.db = db
        self.host = host
        self.resolve_port()

    def as_string(self):
        return u'redis://{}:{}/{}'.format(self.service_ip, self.port, self.db)
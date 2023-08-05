import psycopg2
from . import config

class DatabasePush(object):

    def __init__(self, user, **kwargs):
        self.__dict__.update(kwargs)
        if not hasattr(self, 'secret'):
            self.secret = config.get('db_env_postgres_password', 'secret')
        if not hasattr(self, 'db'):
            self.db = config.get('db_env_db', 'postgres')
        if not hasattr(self, 'user'):
            self.posuser = config.get('db_env_postgres_user', 'postgres')
        if not hasattr(self, 'host'):
            self.host = config.get('db_post_5432_tcp_addr', 'vsrv-sgm-data-01.clsi.ca')
        if not hasattr(self, 'port'):
            self.port = config.get('db_port_5432_tcp_port', '5080'),
        self.domains = []
        self.username = user

    def __enter__(self):
        self.connection = psycopg2.connect(database=self.db, user=self.posuser, password=self.secret, host=self.host, port='5080')
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, *args):
        if self.connection:
            self.connection.commit()
            self.connection.close()



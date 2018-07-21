from os import environ

class Configuration(object):
    def __init__(self):
        ENV = dict(environ)

        try:
            self.debug = ENV['WGADMIN_DEBUG']
        except KeyError:
            self.debug = False

        try:
            self.mysql_hostname = ENV['WGADMIN_DB_HOSTNAME']
        except KeyError:
            self.mysql_hostname = '127.0.0.1'

        try:
            self.mysql_port = int(ENV['WGADMIN_DB_PORT'])
        except KeyError:
            self.mysql_port = 3306

        try:
            self.mysql_username = ENV['WGADMIN_DB_USERNAME']
        except KeyError:
            self.mysql_username = 'root'

        try:
            self.mysql_password = ENV['WGADMIN_DB_PASSWORD']
        except KeyError:
            self.mysql_password = None

        try:
            self.mysql_database = ENV['WGADMIN_DB_NAME']
        except KeyError:
            self.mysql_database = 'wgadmin'

CONF = Configuration()

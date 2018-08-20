from os import environ

class Configuration():
    def __init__(self):
        env = dict(environ)

        try:
            self.debug = env['WGADMIN_DEBUG']
        except KeyError:
            self.debug = False

        try:
            self.mysql_hostname = env['WGADMIN_DB_HOSTNAME']
        except KeyError:
            self.mysql_hostname = '127.0.0.1'

        try:
            self.mysql_port = int(env['WGADMIN_DB_PORT'])
        except KeyError:
            self.mysql_port = 3306

        try:
            self.mysql_username = env['WGADMIN_DB_USERNAME']
        except KeyError:
            self.mysql_username = 'root'

        try:
            self.mysql_password = env['WGADMIN_DB_PASSWORD']
        except KeyError:
            self.mysql_password = None

        try:
            self.mysql_database = env['WGADMIN_DB_NAME']
        except KeyError:
            self.mysql_database = 'wgadmin'

        try:
            self.session_key = env['WGADMIN_SESSION_KEY']
        except KeyError:
            print("WGADMIN_SESSION_KEY environment variable must be specified.")
            exit(1)

        try:
            self.scrypt_n = int(env['WGADMIN_SCRYPT_N'])
        except KeyError:
            self.scrypt_n = 16384

        try:
            self.scrypt_r = int(env['WGADMIN_SCRYPT_R'])
        except KeyError:
            self.scrypt_r = 8

        try:
            self.scrypt_p = int(env['WGADMIN_SCRYPT_P'])
        except KeyError:
            self.scrypt_p = 1

        try:
            self.TOKEN_DURATION = int(env['WGADMIN_TOKEN_DURATION'])
        except KeyError:
            self.token_duration = 1

CONF = Configuration()

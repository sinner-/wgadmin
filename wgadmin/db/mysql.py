import pymysql
from flask import g
from wgadmin.common.config import CONF
from wgadmin.api import app

def get_db():

    database = getattr(g, '_database', None)
    if database is None:
        g._database = pymysql.connect(
            host=CONF.mysql_hostname,
            port=CONF.mysql_port,
            user=CONF.mysql_username,
            passwd=CONF.mysql_password,
            db=CONF.mysql_database
        )

        database = g._database
    return database

@app.teardown_appcontext
def close_connection(exception):
    database = getattr(g, '_database', None)
    if database is not None:
        database.close()

def query_db(query, args=(), one=False):
    cur = get_db().cursor()
    cur.execute(query, args)
    results = cur.fetchall()
    cur.close()
    return (results[0] if results else None) if one else results

def create_tables():

    tables = [
        '''
        CREATE TABLE users (
            username VARCHAR(65) PRIMARY KEY NOT NULL,
            password VARCHAR(255) NOT NULL,
            salt VARCHAR(25) NOT NULL
        );
        ''',
        '''
        CREATE TABLE pubkeys (
            pubkey VARCHAR(45) PRIMARY KEY NOT NULL,
            username VARCHAR(65) NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        );
        '''
    ]

    with app.app_context():
        for table in tables:
            query_db(table)

def drop_tables():

    tables = [
        'pubkeys',
        'users'
    ]

    with app.app_context():
        for table in tables:
            query_db('DROP TABLE IF EXISTS %s;' % table)

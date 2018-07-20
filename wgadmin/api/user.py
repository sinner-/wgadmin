from base64 import b64encode
from hashlib import scrypt
from crypt import mksalt
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import abort
from wgadmin.db.mysql import query_db
from wgadmin.db.mysql import get_db

class User(Resource):

    @staticmethod
    def put(username):
        parser = reqparse.RequestParser()
        parser.add_argument('password',
                            type=str,
                            required=True,
                            help="password is either blank or incorrect type.")
        args = parser.parse_args()

        #check if user exists already
        check_user = query_db('''
                              SELECT username
                              FROM users
                              WHERE username=%s;''',
                              (username,),
                              one=True)
        if check_user is not None:
            abort(422, message="username already registered.")

        encoded_hashed_pw = b64encode(
            hashlib.scrypt(
                password = args.password.encode(),
                salt = mksalt(),
                n = 16384,
                r = 8,
                p = 32
            )
        ).decode()

        #otherwise, add user
        query_db('''
                 INSERT INTO users
                 VALUES(%s, %s);''',
                 (username,
                  encoded_hashed_pw))
        get_db().commit()

        return "User %s registered successfully." % username, 201

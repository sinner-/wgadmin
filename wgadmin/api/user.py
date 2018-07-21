from base64 import b64encode
from hashlib import scrypt
from crypt import mksalt
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import abort
from wgadmin.db.mysql import query_db
from wgadmin.db.mysql import get_db
from wgadmin.common.config import CONF

class User(Resource):

    @staticmethod
    def put(username):
        parser = reqparse.RequestParser()

        parser.add_argument(
            'password',
            type=str,
            required=True,
            help="Either blank or incorrect type."
        )

        args = parser.parse_args()

        #check if user exists already
        check_user = query_db(
            '''
            SELECT username
            FROM users
            WHERE username=%s;
            ''',
            (username,),
            one=True
        )
        if check_user is not None:
            abort(422, message="Username already registered.")

        #hash password
        salt = mksalt()
        encoded_hashed_pw = b64encode(
            scrypt(
                password=args.password.encode(),
                salt=salt.encode(),
                n=CONF.scrypt_n,
                r=CONF.scrypt_r,
                p=CONF.scrypt_p
            )
        ).decode()

        #add user
        query_db(
            '''
            INSERT INTO users(
                username,
                password,
                salt
            )
            VALUES(%s, %s, %s);
            ''',
           (username, encoded_hashed_pw, salt)
        )
        get_db().commit()

        return {"message": "User %s registered successfully." % username}, 201

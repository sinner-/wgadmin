import hmac
import json
import datetime
from base64 import b64encode
from hashlib import scrypt
from hashlib import sha512
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import abort
from wgadmin.db.mysql import query_db
from wgadmin.db.mysql import get_db
from wgadmin.common.config import CONF

class Session(Resource):

    @staticmethod
    def post():
        parser = reqparse.RequestParser()

        parser.add_argument(
            'username',
            type=str,
            required=True,
            help="Either blank or incorrect type."
        )
        parser.add_argument(
            'password',
            type=str,
            required=True,
            help="Either blank or incorrect type."
        )

        args = parser.parse_args()

        #check if user exists
        check_user = query_db(
            '''
            SELECT username, password, salt
            FROM users
            WHERE username=%s;
            ''',
            (args.username,),
            one=True
        )
        if check_user is None:
            abort(422, message="Username doesn't exist.")

        #verify user
        encoded_hashed_pw = b64encode(
            scrypt(
                password=args.password.encode(),
                salt=check_user[2].encode(),
                n=CONF.scrypt_n,
                r=CONF.scrypt_r,
                p=CONF.scrypt_p
            )
        ).decode()

        if check_user[1] != encoded_hashed_pw:
            abort(403, message="Login failed.")

        #generate session
        payload = b64encode(
            json.dumps(
                {
                    'username': args.username,
                    'iat': datetime.datetime.now().timestamp()
                }
            ).encode()
        )

        signature = b64encode(
            hmac.new(
                key=CONF.session_key.encode(),
                msg=payload,
                digestmod=sha512
            ).digest()
        ).decode()

        return {"token": "%s.%s" % (payload.decode(), signature)}, 200

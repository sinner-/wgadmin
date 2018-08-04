import json
import datetime
from base64 import b64encode
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import abort
from wgadmin.db.mysql import query_db
from wgadmin.util.password import encode_hash_pw
from wgadmin.util.token import sign
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
            SELECT username, role, password, salt
            FROM users
            WHERE username=%s;
            ''',
            (args.username,),
            one=True
        )
        if check_user is None:
            abort(403, message="Login failed.")

        #verify user
        encoded_hashed_pw = encode_hash_pw(args.password, check_user[3])

        if check_user[2] != encoded_hashed_pw:
            abort(403, message="Login failed.")

        #generate session
        payload = b64encode(
            json.dumps(
                {
                    'username': args.username,
                    'role': check_user[1],
                    'iat': datetime.datetime.now().timestamp()
                }
            ).encode()
        )

        signature = sign(CONF.session_key.encode(), payload)

        return {"token": "%s.%s" % (payload.decode(), signature)}, 200

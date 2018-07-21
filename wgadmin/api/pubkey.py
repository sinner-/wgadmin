from base64 import b64decode
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import abort
from wgadmin.db.mysql import query_db
from wgadmin.db.mysql import get_db
from wgadmin.util.token import check_auth

class PublicKey(Resource):

    @staticmethod
    def post():
        parser = reqparse.RequestParser()

        parser.add_argument(
            'Authorization',
            type=str,
            location='headers',
            required=True,
            help="Either blank or incorrect type."
        )
        parser.add_argument(
            'pubkey',
            type=str,
            required=True,
            help="Either blank or incorrect type."
        )

        args = parser.parse_args()

        #check auth
        auth = check_auth(args.Authorization)
        if not auth:
            abort(403, message="Unauthorized.")

        #input validation
        try:
            if len(args.pubkey) != 44:
                raise Exception
            b64decode(args.pubkey)
        except:
            abort(400, message="Invalid Public Key.")

        query_db(
            '''
            INSERT INTO pubkeys (
                pubkey,
                username
            )
            VALUES(%s, %s);
            ''',
            (args.pubkey, auth['username'])
        )
        get_db().commit()

        return {"message": "Public Key successfully saved."}, 201

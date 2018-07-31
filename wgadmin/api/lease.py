from base64 import b64decode
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import abort
from wgadmin.db.mysql import query_db
from wgadmin.db.mysql import get_db
from wgadmin.util.token import check_auth

class Lease(Resource):

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
            UPDATE leases
            SET pubkey = %s
            WHERE pubkey IS NULL
            LIMIT 1
            ''',
            (args.pubkey)
        )
        get_db().commit()

        ip = query_db(
            '''
            SELECT ip
            FROM leases
            WHERE pubkey = %s
            ''',
            (args.pubkey),
            one=True
        )

        return {"lease": ip[0]}, 201

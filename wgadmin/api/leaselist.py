from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import abort
from wgadmin.db.mysql import query_db
from wgadmin.util.token import check_auth

class LeaseList(Resource):

    @staticmethod
    def get():
        parser = reqparse.RequestParser()

        parser.add_argument(
            'Authorization',
            type=str,
            location='headers',
            required=True,
            help="Either blank or incorrect type."
        )

        args = parser.parse_args()

        #check auth
        auth = check_auth(args.Authorization)
        if not auth or auth['role'] not in ("admin", "server"):
            abort(403, message="Unauthorized.")

        result = query_db(
            '''
            SELECT ip, pubkey
            FROM leases
            '''
        )

        leases = []

        for row in result:
            leases.append({"ip": row[0], "pubkey": row[1]})

        return {"leases": leases}, 200

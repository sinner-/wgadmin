from crypt import mksalt
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import abort
from wgadmin.db.mysql import query_db
from wgadmin.db.mysql import get_db
from wgadmin.util.token import check_auth
from wgadmin.util.password import encode_hash_pw

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
        parser.add_argument(
            'role',
            type=str,
            required=False,
            default='user',
            help="Either blank or incorrect type."
        )
        parser.add_argument(
            'Authorization',
            type=str,
            location='headers',
            default='unauthorized',
            required=False,
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

        if args.role != "user":
            auth = check_auth(args.Authorization)
            if not auth or auth['role'] != "admin":
                abort(403, message="Unauthorized.")

        #hash password
        salt = mksalt()
        encoded_hashed_pw = encode_hash_pw(args.password, salt)

        #add user
        query_db(
            '''
            INSERT INTO users(
                username,
                role,
                password,
                salt
            )
            VALUES(%s, %s, %s, %s);
            ''',
            (username, args.role, encoded_hashed_pw, salt)
        )
        get_db().commit()

        return {"message": "User %s registered successfully." % username}, 201

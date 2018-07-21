from wgadmin.api import api
from wgadmin.api.user import User
from wgadmin.api.session import Session
from wgadmin.api.key import Key

api.add_resource(User, '/api/v1.0/user/<username>')
api.add_resource(Session, '/api/v1.0/session')
api.add_resource(Key, '/api/v1.0/user/me/key/<keyid>')

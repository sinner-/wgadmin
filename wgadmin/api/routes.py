from wgadmin.api import api
from wgadmin.api.user import User
from wgadmin.api.session import Session
from wgadmin.api.pubkey import PublicKey
from wgadmin.api.lease import Lease

api.add_resource(User, '/api/v1.0/user/<username>')
api.add_resource(Session, '/api/v1.0/session')
api.add_resource(PublicKey, '/api/v1.0/user/me/pubkeys')
api.add_resource(Lease, '/api/v1.0/user/me/lease')

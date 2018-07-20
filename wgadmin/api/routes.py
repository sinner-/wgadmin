from wgadmin.api import api
from wgadmin.api.user import User
from wgadmin.api.session import Session

api.add_resource(User, '/api/v1.0/users/<username>')

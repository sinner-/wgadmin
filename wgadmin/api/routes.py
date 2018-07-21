from wgadmin.api import api
from wgadmin.api.user import User

api.add_resource(User, '/api/v1.0/users/<username>')

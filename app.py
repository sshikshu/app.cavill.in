"""
app
"""

import falcon

from middlewares import AuthMiddleware
from user import AuthResource, UsersResource

api = falcon.API(middleware=([AuthMiddleware()]))

api.add_route('/users', UsersResource())
api.add_route('/users/auth/login', AuthResource())

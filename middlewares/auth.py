"""
middlewares for the api
"""

import falcon
import jwt

from constants import *


class AuthMiddleware(object):
    def process_resource(self, req, _res, resource):
        try:
            token = req.get_header('X-Auth-Token')

            resource.auth_error = None
            resource.user = {}

            if token is None:
                description = 'Please provide an auth token as part of the request.'
                resource.auth_error = falcon.HTTPUnauthorized('Auth token not present', description)

            else:
                resource.user = jwt.decode(token, AUTH_SECRET)
        except jwt.DecodeError:
            description = 'The provided auth token is not valid. Please request a new token and try again.'
            req.auth_error = falcon.HTTPUnauthorized('Authentication required', description, scheme='Token; UUID')
        except Exception as ex:
            print(ex)
            resource.auth_error = falcon.HTTPInternalServerError('Internal Server Error', ERROR_GENERAL)

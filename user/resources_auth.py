"""
auth resources
"""

import json

import falcon
import jwt

from constants import *
from db import conn, r
from hooks import validate_json
from user.schema import user_schema_auth, user_schema_internal


class AuthResource(object):
    def __init__(self):
        self.parsing_schema = user_schema_auth

    @falcon.before(validate_json)
    def on_post(self, _req: falcon.Request, res: falcon.Response):
        print(self.data)
        if 'nickname' not in self.data or 'password' not in self.data:
            raise falcon.HTTPUnauthorized('nickname or password missing', ERROR_INVALID_DATA_SUPPLIED)
        user = r.db(DB_NAME).table(DB_TABLE_USERS).get(self.data['nickname']).run(conn)
        if user['password'] != self.data['password']:
            raise falcon.HTTPUnauthorized('invalid nickname or password', ERROR_INVALID_DATA_SUPPLIED)
        web_token = jwt.encode(user_schema_internal.load(data=user).data, AUTH_SECRET).decode()
        res.body = json.dumps({'token': web_token})

"""
user resources
"""

import json
import time

import falcon

from constants import *
from db import conn, r
from hooks import validate_json
from user.schema import user_schema_client, user_schema_external, user_schema_internal


class UsersResource(object):
    def __init__(self):
        self.auth_error = None
        self.data = None
        self.parsing_schema = user_schema_client
        self.user = {}

    def on_get(self, req: falcon.Request, res: falcon.Response):
        nickname = req.get_param('nickname')
        if nickname:
            user = r.db(DB_NAME).table(DB_TABLE_USERS).get(nickname).run(conn)
            if self.user and self.user['nickname'] == user['nickname']:
                response = user_schema_internal.dumps(user)
            else:
                response = user_schema_external.dumps(user)
        else:
            users = r.db(DB_NAME).table(DB_TABLE_USERS).run(conn)
            response = user_schema_external.loads(list(users), many=True)
        res.body = response.data

    @falcon.before(validate_json)
    def on_post(self, _req: falcon.Request, res: falcon.Response):
        # todo: use salted password
        self.data['created_on'] = int(time.time() * 1000)
        result = r.db(DB_NAME).table(DB_TABLE_USERS).insert(self.data).run(conn)
        res.body = json.dumps(result)

    @falcon.before(validate_json)
    def on_patch(self, req: falcon.Request, res: falcon.Response):
        # todo: use salted password
        if self.auth_error:
            raise self.auth_error
        nickname = req.get_param('nickname')
        if not nickname:
            raise falcon.HTTPMethodNotAllowed(ERROR_INVALID_REQUEST)
        if self.user and self.user['nickname'] == nickname:
            result = r.db(DB_NAME).table(DB_TABLE_USERS).update(self.data).run(conn)
            res.body = json.dumps(result)
        else:
            raise falcon.HTTPUnauthorized('Unauthorized Error', ERROR_INVALID_REQUEST)

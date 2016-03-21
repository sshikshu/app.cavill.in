"""
hooks for resource user
"""

import falcon
from marshmallow import ValidationError

from constants import *


def validate_json(req, _res, resource, _params):
    try:
        partial = req.method != 'POST'
        resource.data, _ = resource.parsing_schema.loads(req.stream.read().decode('utf-8'), partial=partial)
    # todo: check if jsondecodeerror is required
    except ValidationError:
        raise falcon.HTTPBadRequest('Bad Request', ERROR_INVALID_DATA_SUPPLIED)
    except Exception:
        raise falcon.HTTPInternalServerError('Internal Server Error', ERROR_GENERAL)

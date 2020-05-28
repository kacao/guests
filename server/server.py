import asyncio
from aiohttp import web
import json
import logging
from sanic import Sanic, response
from .utils import *
from .voucher import Vouchers

logger = logging.getLogger(__name__)
UPDATE_INTERVAL = 60

API = 'api'
ROUTE_VOUCHERS = 'vouchers'

RC_ERROR = 'err'

def unifi_api_check(f):
    """ return 500 server error if ApiError is caught """
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except ApiError as err:
            logger.error(err)
            return response.json(_make_error_response("internal server error"), status=500)
    return wrapper

class ApiServer:

    def __init__(self, host="0.0.0.0", port='8083', api_keys=[]):
        self.host = host
        self.port = port
        self.api_keys = api_keys
        self._stopping = False
        self.app = Sanic()
        self.vouchers = Vouchers()

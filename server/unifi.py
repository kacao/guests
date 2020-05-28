import json
import logging
import httpx
from .utils import ApiError

EP_API = 'api'
EP_LOGIN = 'login'
EP_LOGOUT = 'logout'
EP_SITE = 's'
EP_CMD = 'cmd'
EP_STAT = 'stat'
EP_HOTSPOT ='hotspot'
CMD_CREATE_VOUCHER = 'create-voucher'
CMD_DELETE_VOUCHER = 'delete-voucher'
STAT_LIST_VOUCHER = 'voucher'
DEFAULT_PORT = 8443
DEFAULT_SITE = 'default'
USERNAME = 'username'
PASSWORD = 'password'

API_ERR_LOGIN_REQUIRED = 'api.err.LoginRequired'
logger = logging.getLogger(__name__)

class UnifiClient:

    def __init__(self, username, password, host, port=DEFAULT_PORT,
                 site_id=DEFAULT_SITE, verify_ssl=False):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.verify_ssl = verify_ssl
        self.url = "https://%s:%s/%s" % (self.host, self.port, EP_API)
        self.site_url = "%s/s/%s" % (self.url, site_id)
        self.site_id = site_id
        self.vouchers = {}
        self._closing = False

    def _raise_if_api_error(self, res, j):
        if res.status_code != 200:
            msg = res['meta']['msg']
            logger.error(logger.error(msg))
            raise ApiError(msg)

        if 'meta' in j:
            if j['meta']['rc'] != 'ok':
                logger.error(j['meta']['msg'])
                raise ApiError(j['meta']['msg'])

        
    async def _req(self, url, method='GET', params=None):
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:

            """ login """
            res = await client.post(self.url + "/" + EP_LOGIN,
                json={USERNAME: self.username, PASSWORD: self.password})
            j = res.json()
            self._raise_if_api_error(res, j)

            """ successfully logged in """
            if method == 'GET':
                res = await client.get(url, params=params)
            elif method == 'POST':
                res = await client.post(url, json=params)
            elif method == 'DELETE':
                res = await client.delete(url, params=params)
            elif method == 'PUT':
                res = await client.put(url, json=params)

            j = res.json()
            self._raise_if_api_error(res, j)

            if 'data' in j:
                return j['data']
            else:
                return j

    async def _get(self, end_point, params=None):
        logger.debug("getting %s%s" % (self.site_url, end_point))
        return await self._req("%s/%s" % (self.site_url, end_point), 'GET', params)

    async def _post(self, end_point, params={}):
        url = "%s/%s" % (self.site_url, end_point)
        logger.debug('cmd %s' % url)
        return await self._req(url, 'POST', params)

    async def _cmd(self, end_point, params={}):
        url = "%s/%s/%s" % (self.site_url, EP_CMD, end_point)
        logger.debug('cmd %s' % url)
        return await self._req(url, 'POST', params)
        
    async def close(self):
        pass

    async def list_vouchers(self):
        ep = "%s/%s" % (EP_STAT, STAT_LIST_VOUCHER)
        return await self._get(ep)

    async def create_voucher(self, number, quota, expire, up_bandwidth=None, down_bandwidth=None, note=None):
        params = {
            'cmd': CMD_CREATE_VOUCHER,
            'n': number,
            'quota': quota,
            'expire': 'custom',
            'expire_number': expire,
            'expire_unit': 1
        }
        if up_bandwidth:
            params['up_bandwidth'] = up_bandwidth
        if down_bandwidth:
            params['down_bandwidth'] = down_bandwidth
        if note:
            params['note'] = note

        return await self._cmd(EP_HOTSPOT, params)

    async def delete_voucher(self, voucher_id):
        params = {
            'cmd': CMD_DELETE_VOUCHER,
            '_id': voucher_id
        }

        return await self._cmd(EP_HOTSPOT, params)

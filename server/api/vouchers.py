from ..utils import _ok_response, _error_response, ApiError
from sanic import Blueprint, response
import logging

json = response.json

logger = logging.getLogger('api/vouchers')

blueprint = Blueprint('vouchers', url_prefix='/vouchers')

@blueprint.exception(ApiError)
def unifi_api_error(req, exception):
    logger.error('api error: ', exception)
    return _error_response("internal server error", status=500)

@blueprint.get('/')
async def list_vouchers_handler(req):
    """
    Command handler for listing vouchers
    """
    unifi = req.ctx.unifi
    vouchers = req.ctx.vouchers

    if vouchers.get_list() == None:
        await _refresh_vouchers(unifi, vouchers)

    return _ok_response(data=vouchers.get_list(), status=200)

@blueprint.post('/')
async def create_voucher(req):
    """
    post /vouchers
    """
    unifi = req.ctx.unifi
    vouchers = req.ctx.vouchers
    data = req.json

    if not 'n' in data:
        data['n'] = 1

    if not 'quota' in data:
        data['quota'] = 0

    if not 'expire' in data:
        data['expire'] = 3600

    if not 'up_bandwidth' in data:
        data['up_bandwidth'] = None

    if not 'down_bandwidth' in data:
        data['down_bandwidth'] = None

    if not 'note' in data:
        data['note'] = None

    res = await unifi.create_voucher(
            data['n'], 
            data['quota'], 
            data['expire'], 
            data['up_bandwidth'], 
            data['down_bandwidth'], 
            data['note'])

    await _refresh_vouchers(unifi, vouchers)
    return _ok_response(data=res, status=200)

async def _refresh_vouchers(unifi, vouchers):
    res = await unifi.list_vouchers()
    vouchers.reset(res)
    logger.info('voucher refreshed')
    logger.info(vouchers.get_list())

@blueprint.delete('/<voucher_id>')
async def delete_voucher(req, voucher_id):
    """
    delete a voucher
    """
    unifi = req.ctx.unifi
    vouchers = req.ctx.vouchers
    
    res = await unifi.delete_voucher(voucher_id)
    await _refresh_vouchers(unifi, vouchers)
    return _ok_response(data=res, status=200)

import json
import logging
import asyncio
from .unifi import UnifiClient
from .data import Vouchers
from sanic import Sanic
from .api import blueprint

CONFIG_FILE = './config.json'
with open(CONFIG_FILE) as f:
    dat = json.load(f)

logging.basicConfig(
    filename=dat['logging']['to_file'],
    level=dat['logging']['level'],
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

async def main():
    uc = dat['unifi_controller']
    sc = dat['server']

    logger.debug('--- starting ---')
    logger.debug(uc)
    logger.debug(sc)
    vouchers = Vouchers()
    unifi = UnifiClient(uc['username'], uc['password'], uc['host'], uc['port'], uc['site_id'], uc['verify_ssl'])
    app = Sanic()

    app.static('/', './app');
    api_coro = app.create_server(host=sc['host'], port=sc['port'], return_asyncio_server=True)
    app.blueprint(blueprint)

    async def unifi_client():
        while True:
            await asyncio.sleep(30)

    @app.middleware('request')
    async def attach_unifi(request):
        """
        Middleware to attach objects to api's server request's context
        """
        request.ctx.unifi = unifi
        request.ctx.api = app
        request.ctx.vouchers = vouchers
        request.ctx.api_keys = sc['api_keys']

    unifi_task = asyncio.create_task(unifi_client())
    api_task = asyncio.create_task(api_coro)
    loop = asyncio.get_running_loop()

    async def close():
        unifi_task.cancel()
        api_task.cancel()

    try:
        await unifi_task
        await api_task
    finally:
        logging.debug('closing')
        unifi_task.cancel()
        api_task.cancel()


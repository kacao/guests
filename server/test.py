import trio
import httpx

async def main():
    session = httpx.AsyncClient(verify=False)
    url = 'https://guinida.tealatte.co:8443/api/stat/voucher'
    res = await session.post(url)
    print(res)

trio.run(main)

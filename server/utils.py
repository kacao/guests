from sanic import response

RC_ERROR = 'err'

class ApiError(Exception):
    pass

def r(*args):
    return "".join(args)

def _ok_response(data=None, status=200):
    res = {'meta': {'rc': 'ok'}}
    if data:
        res['data'] = data
    return response.json(res, status=status)

def _update_response(data=None, status=200):
    res = {'meta':{'a': 'u'}}
    if data:
        res['data'] = data
    return response.json(res, status=status)

def _error_response(msg=None, status=500):
    res = {'meta': {'rc': RC_ERROR, 'msg': msg}}
    if msg:
        res['meta']['msg'] = msg
    return response.json(res, status=status)


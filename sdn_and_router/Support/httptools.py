from sdn_and_router.NET.base import *
from http.client import HTTPConnection


def doHTTP(method, url, Rdata):
    connect = HTTPConnection(FLOODLIGHT_IP, FLOODLIGHT_PORT)
    data = json.dumps(Rdata)
    connect.request(method, url, data, HEADERS)
    resraw = connect.getresponse()
    res = json.loads(resraw.read().decode())
    connect.close()
    if method == 'GET':
        return res
    else:
        return resraw.status



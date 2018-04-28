import json

FLOODLIGHT_IP = '10.201.16.85'
FLOODLIGHT_PORT = 8080
GET_SWITCH_URL = '/wm/core/controller/switches/json'
GET_LINK_URL = '/wm/topology/links/json'
ADD_FLOW_URL = '/wm/staticflowpusher/json'
LIST_ALL_FLOW = '/wm/staticentrypusher/list/all/json'
CLEAR_ALL_FLOW = '/wm/staticflowpusher/clear/all/json '
DEVICE_SHOW = '/wm/device/'
HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
}
GET_BODY = {}

import json

FLOODLIGHT_IP = '10.201.16.70'
FLOODLIGHT_PORT = 8080
ENALBLE_STATISTICS = '/wm/statistics/config/enable/json'
GET_SWITCH_URL = '/wm/core/controller/switches/json'
GET_LINK_URL = '/wm/topology/links/json'
ADD_FLOW_URL = '/wm/staticflowpusher/json'
LIST_ALL_FLOW = '/wm/staticentrypusher/list/all/json'
CLEAR_ALL_FLOW = '/wm/staticflowpusher/clear/all/json '
GET_BANDWIDTH = '/wm/statistics/bandwidth/'
DEVICE_SHOW = '/wm/device/'
SCR_SWITCH = '00:00:00:00:00:00:00:01'
DST_SWITCH = '00:00:00:00:00:00:00:07'
HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
}
GET_BODY = {}

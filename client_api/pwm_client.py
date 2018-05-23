import requests
import json

# Router IDs
THROTTLE = 'throttle'
STEERING = 'steering'

_SERVER_PORT = 5000
_PREFIX = ':' + str(_SERVER_PORT) +'/pwmmgr/api/v1'

# -----------------------------------------------------------------------------
# API
# -----------------------------------------------------------------------------

def get_routers(host):
    result = requests.get('http://' + host + _PREFIX + '/routers')

    if result.status_code == requests.codes.ok:
        return json.loads(result.text)['routers']
    else:
        result.raise_for_status()

# -----------------------------------------------------------------------------
def get_router(host, router_id):
    result = requests.get('http://' + host + _PREFIX + '/routers/' + router_id)

    if result.status_code == requests.codes.ok:
        return json.loads(result.text)['router']
    else:
        result.raise_for_status()

# -----------------------------------------------------------------------------
def get_source(host, router_id):
    result = requests.get('http://' + host + _PREFIX + '/routers/' + router_id + '/source')

    if result.status_code == requests.codes.ok:
        return result.text
    else:
        result.raise_for_status()

# -----------------------------------------------------------------------------
def update_source(host, router_id, source):
    payload = {'source': source}
    result = requests.put('http://' + host + _PREFIX + '/routers/' + router_id + '/source', params=payload)

    if result.status_code == requests.codes.ok:
        return 0
    else:
        result.raise_for_status()

# -----------------------------------------------------------------------------
def get_pulse_width_out(host, router_id):
    result = requests.get('http://' + host + _PREFIX + '/routers/' + router_id + '/pulse_width_out')

    if result.status_code == requests.codes.ok:
        return int(result.text)
    else:
        result.raise_for_status()

# -----------------------------------------------------------------------------
def update_pulse_width_out(host, router_id, pulse_width_usec):
    payload = {'pulse_width': str(pulse_width_usec)}
    result = requests.put('http://' + host + _PREFIX + '/routers/' + router_id + '/pulse_width_out', params=payload)

    if result.status_code == requests.codes.ok:
        return 0
    else:
        result.raise_for_status()

# -----------------------------------------------------------------------------
def get_pulse_width_in(host, router_id):
    result = requests.get('http://' + host + _PREFIX + '/routers/' + router_id + '/pulse_width_in')

    if result.status_code == requests.codes.ok:
        return int(result.text)
    else:
        result.raise_for_status()


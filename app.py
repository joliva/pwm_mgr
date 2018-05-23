from pwm_mgr import PwmMgr
from flask import Flask, jsonify, abort, request, make_response, url_for

pwm_mgr = PwmMgr()

app = Flask(__name__, static_url_path = "")

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

def make_public_router(router):
    new_router = {}
    for field in router:
        new_router[field] = router[field]
        if field == 'id':
            new_router['uri'] = url_for('get_router', router_id = router['id'], _external = True)
    return new_router
    
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@app.route('/pwmmgr/api/v1/routers', methods = ['GET'])
def get_routers():
    return jsonify({'routers': [make_public_router(router) for router in pwm_mgr.routers]})

@app.route('/pwmmgr/api/v1/routers/<string:router_id>', methods = ['GET'])
def get_router(router_id):
    router = [router for router in pwm_mgr.routers if router['id'] == router_id]
    if len(router) == 0:
        abort(404)
    return jsonify( { 'router': make_public_router(router[0]) } )

@app.route('/pwmmgr/api/v1/routers/<string:router_id>', methods = ['PUT'])
def update_router(router_id):
    print(pwm_mgr.routers)
    router = [router for router in pwm_mgr.routers if router['id'] == router_id]
    if len(router) == 0:
        abort(404)
    if not request.json:
        abort(400)

    source = request.json.get('source', router[0]['source'])
    pulse_width_usec = request.json.get('pulse_width_usec', router[0]['pulse_width_usec'])

    if router_id == PwmMgr.ROUTER_THROTTLE:
        pwm_mgr.set_pwm_source(pwm_mgr.throttle, source)
        pwm_mgr.set_pulse_width(pwm_mgr.throttle, pulse_width_usec)
    elif router_id == PwmMgr.ROUTER_STEERING:
        pwm_mgr.set_pwm_source(pwm_mgr.steering, source)
        pwm_mgr.set_pulse_width(pwm_mgr.steering, pulse_width_usec)

    return jsonify( { 'router': make_public_router(router[0]) } )
    
@app.route('/pwmmgr/api/v1/routers/<string:router_id>/source', methods = ['GET'])
def get_source(router_id):
    router = [router for router in pwm_mgr.routers if router['id'] == router_id]
    if len(router) == 0:
        abort(404)
    return router[0]['source']

@app.route('/pwmmgr/api/v1/routers/<string:router_id>/source', methods = ['PUT'])
def update_source(router_id):
    router = [router for router in pwm_mgr.routers if router['id'] == router_id]
    if len(router) == 0:
        abort(404)
    if 'source' in request.args:
        source = request.args['source']

        if source == '': abort(400)
        if not(source == PwmMgr.SOURCE_GPIO or source == PwmMgr.SOURCE_CPU): abort(400)

        if router_id == PwmMgr.ROUTER_THROTTLE:
            pwm_mgr.set_pwm_source(pwm_mgr.throttle, source)
        elif router_id == PwmMgr.ROUTER_STEERING:
            pwm_mgr.set_pwm_source(pwm_mgr.steering, source)

    return router[0]['source']

@app.route('/pwmmgr/api/v1/routers/<string:router_id>/pulse_width_out', methods = ['GET'])
def get_pulse_width_out(router_id):
    router = [router for router in pwm_mgr.routers if router['id'] == router_id]
    if len(router) == 0:
        abort(404)
    return str(router[0]['pulse_width_usec'])

@app.route('/pwmmgr/api/v1/routers/<string:router_id>/pulse_width_out', methods = ['PUT'])
def update_pulse_width(router_id):
    router = [router for router in pwm_mgr.routers if router['id'] == router_id]
    if len(router) == 0:
        abort(404)
    if 'pulse_width' in request.args:
        pw = request.args['pulse_width']
        if RepresentsInt(pw):
            pulse_width_usec = int(pw)
        else:
            abort(400)

        if pulse_width_usec < 0 or pulse_width_usec > 2500: abort(400)

        if router_id == PwmMgr.ROUTER_THROTTLE:
            pwm_mgr.set_pulse_width(pwm_mgr.throttle, pulse_width_usec)
        elif router_id == PwmMgr.ROUTER_STEERING:
            pwm_mgr.set_pulse_width(pwm_mgr.steering, pulse_width_usec)

    return str(router[0]['pulse_width_usec'])

@app.route('/pwmmgr/api/v1/routers/<string:router_id>/pulse_width_in', methods = ['GET'])
def get_pulse_width_in(router_id):
    router = [router for router in pwm_mgr.routers if router['id'] == router_id]
    if len(router) == 0:
        abort(404)

    pw = 0
    if router_id == PwmMgr.ROUTER_THROTTLE:
        pw = pwm_mgr.get_pulse_width_in(pwm_mgr.throttle)
    elif router_id == PwmMgr.ROUTER_STEERING:
        pw = pwm_mgr.get_pulse_width_in(pwm_mgr.steering)

    return str(pw)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
    #app.run(host='0.0.0.0')


# coding: UTF-8

""" RESTful API using Flask"""

from flask import Flask, jsonify, make_response, request, current_app, json
from datetime import timedelta  
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
    """ Function to enable crossdomain calls to the API """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__)


def return_empty():
    """ Function to return a empty JSON object.
    """
    empty = {
            'empty' : "",
            }

    return empty
    
 
""" This is the routing section of the API.
The base URL is http://localhost:5000/
"""    
@app.route('/hcp/api/v1.0/empty/', methods = ['GET'])
@crossdomain(origin='*')
def get_return_empty():
    """ Route for return_empty()
    URL: http://localhost:5000/hcp/api/v1.0/empty/ 
    """
    return jsonify(return_empty())
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
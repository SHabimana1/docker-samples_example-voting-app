from flask import Flask, jsonify, render_template, request, make_response, g
from redis import Redis
from pythonjsonlogger import jsonlogger
import os
import socket
import random
import json
import logging
import time # Added for trace ID generation

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)

# Tracer setup (We rely on Dynatrace OneAgent for tracing hooks now)

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
logHandler.setFormatter(formatter)
app.logger.addHandler(logHandler)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

@app.route("/health")
def health():
    try:
        redis = get_redis()
        redis.ping()
        return "OK", 200
    except Exception as e:
        app.logger.error("Health check failed", extra={'error': str(e)})
        return "Unhealthy", 500

# If the header is stripped, we generate a new one to guarantee context propagation.
def get_guaranteed_traceparent(incoming_header=None):
    # Use incoming header if it exists
    if incoming_header and incoming_header != "null":
        return incoming_header

    # Otherwise, generate a new W3C-compliant trace.
    # Trace ID (16 bytes/32 hex chars) and Span ID (8 bytes/16 hex chars)
    trace_id = hex(random.getrandbits(128))[2:].zfill(32)
    span_id = hex(random.getrandbits(64))[2:].zfill(16)
    
    new_traceparent = f"00-{trace_id}-{span_id}-01"
    
    return new_traceparent

@app.route("/api/vote", methods=['POST'])
def cast_vote_api():
    try:
        voter_id = request.cookies.get('voter_id')
        if not voter_id:
            voter_id = hex(random.getrandbits(64))[2:-1]

        content = request.json
        vote = content['vote']
        
        # Capture Trace Context (look for both standard headers)
        incoming_traceparent = request.headers.get('traceparent')
        if not incoming_traceparent:
            incoming_traceparent = request.headers.get('x-dynatrace-header')

        # Guarantee a traceparent exists
        traceparent = get_guaranteed_traceparent(incoming_traceparent)

        app.logger.info('Vote received via API', extra={
            'vote': vote, 
            'voter_id': voter_id,
            'traceparent_used': traceparent 
        })

        redis = get_redis()
        
        # Inject Trace Context into Redis Payload
        data = json.dumps({
            'voter_id': voter_id, 
            'vote': vote,
            'traceparent': traceparent
        })
        redis.rpush('votes', data)

        resp = jsonify(success=True, message="Vote cast")
        resp.set_cookie('voter_id', voter_id)
        return resp, 200

    except Exception as e:
        app.logger.error("API Error", extra={'error': str(e)})
        return jsonify(success=False, error="Internal Server Error"), 500
    
@app.route("/", methods=['POST','GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        
        # Capture Trace Context (look for standard headers)
        incoming_traceparent = request.headers.get('traceparent')
        if not incoming_traceparent:
            incoming_traceparent = request.headers.get('x-dynatrace-header')
            
        # Guarantee a traceparent exists
        traceparent = get_guaranteed_traceparent(incoming_traceparent)

        app.logger.info('Vote received', extra={
            'vote_choice': vote, 
            'voter_id': voter_id, 
            'app': 'vote-frontend',
            'traceparent_used': traceparent
        })
        
        data = json.dumps({
            'voter_id': voter_id, 
            'vote': vote,
            'traceparent': traceparent
        })
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
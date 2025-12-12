from flask import Flask, jsonify, request, render_template, make_response, g
from redis import Redis
import json
import random
import socket
import os
import logging

from tracing_setup import start_trace_span, get_current_traceparent

app = Flask(__name__)

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

@app.route("/api/vote", methods=['POST'])
def cast_vote_api():
    voter_id = request.cookies.get("voter_id") or hex(random.getrandbits(64))[2:]

    with start_trace_span("vote-api-request"):
        content = request.json
        vote = content["vote"]

        traceparent = get_current_traceparent()

        app.logger.info("Vote received via API", extra={
            "vote": vote,
            "voter_id": voter_id,
            "traceparent_generated": traceparent
        })

        data = json.dumps({
            "vote": vote,
            "voter_id": voter_id,
            "traceparent": traceparent
        })

        redis = get_redis()
        redis.rpush("votes", data)

        resp = jsonify(success=True, message="Vote cast")
        resp.set_cookie("voter_id", voter_id)
        return resp

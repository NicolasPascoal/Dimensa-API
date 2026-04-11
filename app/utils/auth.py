import os
from functools import wraps
from flask import request, jsonify
from config import Config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'Token está faltando!'}), 401

        expected_token = Config.SECRET_TOKEN
        
        if token != expected_token:
            return jsonify({'message': 'Token é inválido!'}), 401

        return f(*args, **kwargs)

    return decorated
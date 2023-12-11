import jwt
from flask import request, jsonify
from functools import wraps
import os

def checkToken(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            payload = jwt.decode(token.split(" ")[1], os.getenv('JWT_KEY'), algorithms=['HS256'])
            if 'email' not in payload:
                print("Invalid Token: Email not present in payload")
                return jsonify({'message': 'Token is invalid!'}), 401
        except jwt.ExpiredSignatureError:
            print("Expired Token")
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            print("Invalid Token")
            return jsonify({'message': 'Token is invalid!'}), 401

        print("Token:", token)
        print("JWT_KEY:", os.getenv('JWT_KEY'))
        print("Decoded Payload:", payload)

        return func(*args, **kwargs)

    return wrapper


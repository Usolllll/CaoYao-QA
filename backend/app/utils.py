from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User

def success_response(data=None, message='Success', code=200):
    """成功响应"""
    response = {
        'success': True,
        'message': message,
        'code': code
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code


def error_response(message='Error', code=400, errors=None):
    """错误响应"""
    response = {
        'success': False,
        'message': message,
        'code': code
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), code


def jwt_required_with_user(fn):
    """JWT验证装饰器，同时获取用户对象"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return error_response('User not found', 404)
        
        return fn(current_user, *args, **kwargs)
    
    return wrapper

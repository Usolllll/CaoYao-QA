from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User, UserStatistics
from app.utils import success_response, error_response

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    # 验证必填字段
    if not data or not data.get('username') or not data.get('password'):
        return error_response('Username and password are required', 400)
    
    username = data.get('username')
    password = data.get('password')
    nickname = data.get('nickname', username)
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return error_response('Username already exists', 400)
    
    # 创建新用户
    user = User(username=username, nickname=nickname)
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # 创建用户统计记录
        statistics = UserStatistics(user_id=user.id)
        db.session.add(statistics)
        db.session.commit()
        
        # 生成访问令牌 - 注意：identity 必须是字符串
        access_token = create_access_token(identity=str(user.id))
        
        return success_response({
            'user': user.to_dict(),
            'access_token': access_token
        }, 'Registration successful', 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Registration failed: {str(e)}', 500)


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return error_response('Username and password are required', 400)
    
    username = data.get('username')
    password = data.get('password')
    
    # 查找用户
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return error_response('Invalid username or password', 401)
    
    # 生成访问令牌 - 注意：identity 必须是字符串
    access_token = create_access_token(identity=str(user.id))
    
    return success_response({
        'user': user.to_dict(),
        'access_token': access_token
    }, 'Login successful')
    return success_response({
        'user': user.to_dict(),
        'access_token': access_token
    }, 'Login successful')


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前用户信息"""
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if not user:
        return error_response('User not found', 404)
    
    return success_response(user.to_dict())


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """用户登出（前端删除token即可）"""
    return success_response(message='Logout successful')

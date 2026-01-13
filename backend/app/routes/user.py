from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, UserStatistics, AnswerRecord
from app.utils import success_response, error_response
from datetime import datetime, timedelta

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户资料"""
    current_user_id = int(get_jwt_identity())
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return error_response('User not found', 404)
    
    statistics = UserStatistics.query.filter_by(user_id=current_user.id).first()
    
    return success_response({
        'user': current_user.to_dict(),
        'statistics': statistics.to_dict() if statistics else None
    })


@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新用户资料"""
    current_user_id = int(get_jwt_identity())
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return error_response('User not found', 404)
    
    data = request.get_json()
    
    if not data:
        return error_response('No data provided', 400)
    
    # 可更新的字段
    if 'nickname' in data:
        current_user.nickname = data['nickname']
    
    if 'avatar' in data:
        current_user.avatar = data['avatar']
    
    try:
        db.session.commit()
        return success_response(current_user.to_dict(), 'Profile updated successfully')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update profile: {str(e)}', 500)


@user_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    """获取用户统计信息"""
    try:
        # get_jwt_identity() 返回字符串，需要转换为整数
        current_user_id = int(get_jwt_identity())
        
        statistics = UserStatistics.query.filter_by(user_id=current_user_id).first()
        
        if not statistics:
            return success_response({
                'total_questions': 0,
                'correct_answers': 0,
                'accuracy_rate': 0,
                'continuous_days': 0
            })
        
        return success_response(statistics.to_dict())
    except Exception as e:
        return error_response(f'Failed to get statistics: {str(e)}', 500)


@user_bp.route('/history', methods=['GET'])
@jwt_required()
def get_answer_history():
    """获取答题历史"""
    current_user_id = int(get_jwt_identity())
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = AnswerRecord.query.filter_by(user_id=current_user_id)\
        .order_by(AnswerRecord.answered_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    records = []
    for record in pagination.items:
        record_dict = record.to_dict()
        # 添加题目信息
        question = record.question
        record_dict['question'] = question.to_dict(include_answer=True)
        records.append(record_dict)
    
    return success_response({
        'records': records,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@user_bp.route('/statistics/weekly', methods=['GET'])
@jwt_required()
def get_weekly_statistics():
    """获取最近一周的答题统计"""
    current_user_id = int(get_jwt_identity())
    
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    
    records = AnswerRecord.query.filter(
        AnswerRecord.user_id == current_user_id,
        AnswerRecord.answered_at >= week_ago
    ).all()
    
    # 按日期统计
    daily_stats = {}
    for i in range(7):
        date = today - timedelta(days=i)
        daily_stats[date.isoformat()] = {
            'total': 0,
            'correct': 0,
            'accuracy': 0
        }
    
    for record in records:
        date_key = record.answered_at.date().isoformat()
        if date_key in daily_stats:
            daily_stats[date_key]['total'] += 1
            if record.is_correct:
                daily_stats[date_key]['correct'] += 1
    
    # 计算正确率
    for date_key in daily_stats:
        if daily_stats[date_key]['total'] > 0:
            daily_stats[date_key]['accuracy'] = round(
                (daily_stats[date_key]['correct'] / daily_stats[date_key]['total']) * 100, 2
            )
    
    return success_response(daily_stats)

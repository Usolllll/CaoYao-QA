from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Question, AnswerRecord, UserStatistics, User
from app.utils import success_response, error_response
import random

question_bp = Blueprint('question', __name__)


@question_bp.route('/random', methods=['GET'])
@jwt_required()
def get_random_question():
    """获取随机题目"""
    # 获取难度参数（可选）
    difficulty = request.args.get('difficulty')
    category = request.args.get('category')
    
    query = Question.query
    
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    
    if category:
        query = query.filter_by(category=category)
    
    # 获取所有符合条件的题目ID
    question_ids = [q.id for q in query.with_entities(Question.id).all()]
    
    if not question_ids:
        return error_response('No questions available', 404)
    
    # 随机选择一个题目
    random_id = random.choice(question_ids)
    question = Question.query.get(random_id)
    
    return success_response(question.to_dict())


@question_bp.route('/<int:question_id>', methods=['GET'])
@jwt_required()
def get_question(question_id):
    """获取指定题目"""
    question = Question.query.get(question_id)
    
    if not question:
        return error_response('Question not found', 404)
    
    return success_response(question.to_dict())


@question_bp.route('/<int:question_id>/answer', methods=['POST'])
@jwt_required()
def submit_answer(question_id):
    """提交答案"""
    current_user_id = int(get_jwt_identity())
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return error_response('User not found', 404)
    
    data = request.get_json()
    
    if not data or not data.get('answer'):
        return error_response('Answer is required', 400)
    
    user_answer = data.get('answer').upper()
    
    if user_answer not in ['A', 'B', 'C', 'D']:
        return error_response('Invalid answer format', 400)
    
    # 获取题目
    question = Question.query.get(question_id)
    if not question:
        return error_response('Question not found', 404)
    
    # 判断答案是否正确
    is_correct = (user_answer == question.correct_answer)
    
    try:
        # 保存答题记录
        record = AnswerRecord(
            user_id=current_user.id,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=is_correct
        )
        db.session.add(record)
        
        # 更新用户统计
        statistics = UserStatistics.query.filter_by(user_id=current_user.id).first()
        if not statistics:
            statistics = UserStatistics(user_id=current_user.id)
            db.session.add(statistics)
        
        statistics.update_statistics(is_correct)
        
        db.session.commit()
        
        return success_response({
            'is_correct': is_correct,
            'correct_answer': question.correct_answer,
            'explanation': question.explanation,
            'statistics': statistics.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to submit answer: {str(e)}', 500)


@question_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """获取所有题目分类"""
    current_user_id = int(get_jwt_identity())
    
    categories = db.session.query(Question.category).distinct().all()
    category_list = [c[0] for c in categories if c[0]]
    
    return success_response(category_list)


@question_bp.route('/list', methods=['GET'])
@jwt_required()
def get_question_list():
    """获取题目列表（分页）"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    difficulty = request.args.get('difficulty')
    category = request.args.get('category')
    
    query = Question.query
    
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    
    if category:
        query = query.filter_by(category=category)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return success_response({
        'questions': [q.to_dict() for q in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })

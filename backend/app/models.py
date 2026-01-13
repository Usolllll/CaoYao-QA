from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(50))
    avatar = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    answer_records = db.relationship('AnswerRecord', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    statistics = db.relationship('UserStatistics', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.Enum('A', 'B', 'C', 'D'), nullable=False)
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.Enum('easy', 'medium', 'hard'), default='medium')
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    answer_records = db.relationship('AnswerRecord', backref='question', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_answer=False):
        result = {
            'id': self.id,
            'question_text': self.question_text,
            'options': {
                'A': self.option_a,
                'B': self.option_b,
                'C': self.option_c,
                'D': self.option_d
            },
            'difficulty': self.difficulty,
            'category': self.category
        }
        
        if include_answer:
            result['correct_answer'] = self.correct_answer
            result['explanation'] = self.explanation
        
        return result


class AnswerRecord(db.Model):
    __tablename__ = 'answer_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False, index=True)
    user_answer = db.Column(db.Enum('A', 'B', 'C', 'D'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'user_answer': self.user_answer,
            'is_correct': self.is_correct,
            'answered_at': self.answered_at.isoformat() if self.answered_at else None
        }


class UserStatistics(db.Model):
    __tablename__ = 'user_statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    total_questions = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    accuracy_rate = db.Column(db.Numeric(5, 2), default=0.00)
    last_study_date = db.Column(db.Date)
    continuous_days = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'accuracy_rate': float(self.accuracy_rate),
            'last_study_date': self.last_study_date.isoformat() if self.last_study_date else None,
            'continuous_days': self.continuous_days
        }
    
    def update_statistics(self, is_correct):
        """更新用户统计信息"""
        self.total_questions += 1
        if is_correct:
            self.correct_answers += 1
        
        # 更新正确率
        if self.total_questions > 0:
            self.accuracy_rate = (self.correct_answers / self.total_questions) * 100
        
        # 更新连续学习天数
        today = datetime.utcnow().date()
        if self.last_study_date:
            if self.last_study_date == today:
                pass  # 同一天，不更新连续天数
            elif (today - self.last_study_date).days == 1:
                self.continuous_days += 1
            else:
                self.continuous_days = 1
        else:
            self.continuous_days = 1
        
        self.last_study_date = today

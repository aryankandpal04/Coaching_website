from datetime import datetime
from app import db
import json

class Test(db.Model):
    __tablename__ = 'tests'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Integer, nullable=False)  # Class 6-12
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    total_marks = db.Column(db.Integer, nullable=False)
    passing_marks = db.Column(db.Integer, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    
    # Test configuration
    allow_retake = db.Column(db.Boolean, default=False)
    show_result_immediately = db.Column(db.Boolean, default=True)
    randomize_questions = db.Column(db.Boolean, default=True)
    
    # Relationships
    questions = db.relationship('Question', backref='test', lazy=True, cascade='all, delete-orphan')
    results = db.relationship('TestResult', backref='test', lazy=True)
    
    def __init__(self, title, subject, grade, creator_id, duration, total_marks, passing_marks, **kwargs):
        self.title = title
        self.subject = subject
        self.grade = grade
        self.creator_id = creator_id
        self.duration = duration
        self.total_marks = total_marks
        self.passing_marks = passing_marks
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<Test {self.title}>'

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # mcq, subjective
    options = db.Column(db.Text)  # JSON string for MCQ options
    correct_answer = db.Column(db.Text, nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    explanation = db.Column(db.Text)
    
    def set_options(self, options_list):
        self.options = json.dumps(options_list)
    
    def get_options(self):
        return json.loads(self.options) if self.options else []

class TestResult(db.Model):
    __tablename__ = 'test_results'
    
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    status = db.Column(db.String(20))  # started, completed, abandoned
    answers = db.Column(db.Text)  # JSON string storing answers
    
    def set_answers(self, answers_dict):
        self.answers = json.dumps(answers_dict)
    
    def get_answers(self):
        return json.loads(self.answers) if self.answers else {}

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='incomplete')  # 'incomplete', 'completed', 'evaluated'
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    answers = db.relationship('Answer', backref='result', lazy='dynamic')

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('result.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer_text = db.Column(db.Text)  # For written answers
    selected_option = db.Column(db.String(1))  # For MCQ answers
    marks_obtained = db.Column(db.Float)
    is_correct = db.Column(db.Boolean)  # For MCQ auto-evaluation
    evaluated_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # For written answers
    evaluation_remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
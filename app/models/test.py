from datetime import datetime
from app import db

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(100), nullable=False)
    class_level = db.Column(db.String(20), nullable=False)
    test_type = db.Column(db.String(20), nullable=False)  # 'mcq' or 'written'
    duration = db.Column(db.Integer)  # in minutes
    total_marks = db.Column(db.Integer, nullable=False)
    passing_marks = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    questions = db.relationship('Question', backref='test', lazy='dynamic')
    results = db.relationship('Result', backref='test', lazy='dynamic')
    
    def __init__(self, title, subject, class_level, test_type, total_marks, passing_marks, creator_id):
        self.title = title
        self.subject = subject
        self.class_level = class_level
        self.test_type = test_type
        self.total_marks = total_marks
        self.passing_marks = passing_marks
        self.creator_id = creator_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'subject': self.subject,
            'class_level': self.class_level,
            'test_type': self.test_type,
            'duration': self.duration,
            'total_marks': self.total_marks,
            'passing_marks': self.passing_marks,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'created_at': self.created_at.isoformat()
        }

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # 'mcq' or 'written'
    marks = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    
    # For MCQ questions
    option_a = db.Column(db.Text)
    option_b = db.Column(db.Text)
    option_c = db.Column(db.Text)
    option_d = db.Column(db.Text)
    correct_option = db.Column(db.String(1))  # 'a', 'b', 'c', or 'd'
    
    # Relationships
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

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
from datetime import datetime
from app import db

class MockTest(db.Model):
    """Model for mock tests"""
    __tablename__ = 'mock_tests'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(20), nullable=False)  # Class/Grade level
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    total_marks = db.Column(db.Integer, nullable=False)
    passing_marks = db.Column(db.Integer, nullable=False)
    
    # Test availability
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Creator info
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('Question', backref='mock_test', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('TestAttempt', backref='mock_test', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<MockTest {self.title}>'
    
    @property
    def is_available(self):
        """Check if the test is currently available"""
        now = datetime.utcnow()
        return self.is_active and self.start_date <= now <= self.end_date
    
    @property
    def question_count(self):
        """Get the number of questions in the test"""
        return len(self.questions)

class Question(db.Model):
    """Model for test questions"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    mock_test_id = db.Column(db.Integer, db.ForeignKey('mock_tests.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # 'mcq', 'true_false', 'short_answer'
    marks = db.Column(db.Integer, nullable=False, default=1)
    
    # For MCQ questions
    option_a = db.Column(db.Text)
    option_b = db.Column(db.Text)
    option_c = db.Column(db.Text)
    option_d = db.Column(db.Text)
    
    # Correct answer
    correct_answer = db.Column(db.Text, nullable=False)
    
    # Optional explanation
    explanation = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Question {self.id}>'

class TestAttempt(db.Model):
    """Model for student test attempts"""
    __tablename__ = 'test_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    mock_test_id = db.Column(db.Integer, db.ForeignKey('mock_tests.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Attempt details
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    is_completed = db.Column(db.Boolean, default=False)
    
    # Results
    score = db.Column(db.Integer)
    percentage = db.Column(db.Float)
    passed = db.Column(db.Boolean)
    
    # Relationships
    answers = db.relationship('Answer', backref='attempt', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<TestAttempt {self.id}>'
    
    @property
    def duration(self):
        """Calculate the duration of the attempt in minutes"""
        if self.end_time:
            delta = self.end_time - self.start_time
            return delta.total_seconds() / 60
        return None

class Answer(db.Model):
    """Model for student answers to questions"""
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('test_attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    
    # Student's answer
    student_answer = db.Column(db.Text)
    
    # Assessment
    is_correct = db.Column(db.Boolean)
    marks_awarded = db.Column(db.Float)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    question = db.relationship('Question', backref='answers')
    
    def __repr__(self):
        return f'<Answer {self.id}>' 
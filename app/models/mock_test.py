from datetime import datetime
from app import db
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Optional

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
    def question_count(self) -> int:
        """Get the number of questions in the test"""
        return len(self.questions.all())
    
    def validate_test_setup(self) -> Dict[str, str]:
        """Validate test setup before activation"""
        errors = {}
        
        questions = self.questions.all()
        if not questions:
            errors['questions'] = 'Test must have at least one question'
            
        if self.start_date >= self.end_date:
            errors['dates'] = 'Start date must be before end date'
            
        if self.passing_marks > self.total_marks:
            errors['marks'] = 'Passing marks cannot exceed total marks'
            
        actual_total = sum(q.marks for q in questions)
        if actual_total != self.total_marks:
            errors['total_marks'] = f'Sum of question marks ({actual_total}) does not match total marks ({self.total_marks})'
            
        return errors
    
    def get_student_result(self, student_id: int) -> Optional[Dict]:
        """Get test result for a specific student"""
        attempt = TestAttempt.query.filter_by(
            mock_test_id=self.id,
            student_id=student_id,
            is_completed=True
        ).first()
        
        if not attempt:
            return None
            
        return {
            'score': attempt.score,
            'percentage': attempt.percentage,
            'passed': attempt.passed,
            'duration': attempt.duration,
            'attempt_date': attempt.start_time
        }
    
    def get_class_statistics(self) -> Dict:
        """Get statistical analysis of test performance"""
        completed_attempts = TestAttempt.query.filter_by(
            mock_test_id=self.id,
            is_completed=True
        ).all()
        
        if not completed_attempts:
            return {
                'total_attempts': 0,
                'pass_rate': 0,
                'average_score': 0,
                'highest_score': 0,
                'lowest_score': 0
            }
        
        scores = [attempt.score for attempt in completed_attempts]
        passed = len([attempt for attempt in completed_attempts if attempt.passed])
        
        return {
            'total_attempts': len(completed_attempts),
            'pass_rate': (passed / len(completed_attempts)) * 100,
            'average_score': sum(scores) / len(scores),
            'highest_score': max(scores),
            'lowest_score': min(scores)
        }

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
    
    def submit_answer(self, question_id: int, answer: str) -> bool:
        """Submit an answer for a question"""
        try:
            question = Question.query.get(question_id)
            if not question or question.mock_test_id != self.mock_test_id:
                return False
                
            existing_answer = Answer.query.filter_by(
                attempt_id=self.id,
                question_id=question_id
            ).first()
            
            if existing_answer:
                existing_answer.student_answer = answer
                existing_answer.is_correct = (answer.strip().lower() == question.correct_answer.strip().lower())
                existing_answer.marks_awarded = question.marks if existing_answer.is_correct else 0
            else:
                new_answer = Answer(
                    attempt_id=self.id,
                    question_id=question_id,
                    student_answer=answer,
                    is_correct=(answer.strip().lower() == question.correct_answer.strip().lower()),
                    marks_awarded=question.marks if answer.strip().lower() == question.correct_answer.strip().lower() else 0
                )
                db.session.add(new_answer)
                
            db.session.commit()
            return True
            
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    def complete_test(self) -> bool:
        """Complete the test attempt and calculate results"""
        try:
            if self.is_completed:
                return False
                
            self.end_time = datetime.utcnow()
            self.is_completed = True
            
            # Calculate score
            answers = self.answers.all()
            total_scored = sum(answer.marks_awarded for answer in answers)
            total_possible = self.mock_test.total_marks
            
            self.score = total_scored
            self.percentage = (total_scored / total_possible) * 100
            self.passed = total_scored >= self.mock_test.passing_marks
            
            db.session.commit()
            return True
            
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    def get_remaining_time(self) -> int:
        """Get remaining time in minutes"""
        if self.is_completed:
            return 0
            
        elapsed = (datetime.utcnow() - self.start_time).total_seconds() / 60
        remaining = self.mock_test.duration - elapsed
        return max(0, int(remaining))
    
    def get_answer_summary(self) -> List[Dict]:
        """Get summary of answers with explanations"""
        answers = self.answers.all()
        return [{
            'question_text': answer.question.question_text,
            'student_answer': answer.student_answer,
            'correct_answer': answer.question.correct_answer,
            'is_correct': answer.is_correct,
            'marks_awarded': answer.marks_awarded,
            'explanation': answer.question.explanation
        } for answer in answers]

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
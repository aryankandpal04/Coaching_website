from datetime import datetime
from app import db

class Doubt(db.Model):
    """Model for student doubts"""
    __tablename__ = 'doubts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Subject and grade
    subject = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(20), nullable=False)  # Class/Grade level
    
    # Status
    status = db.Column(db.String(20), default='open')  # 'open', 'answered', 'closed'
    
    # User info
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))  # Teacher assigned to answer
    
    # Optional references
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))
    mock_test_id = db.Column(db.Integer, db.ForeignKey('mock_tests.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    responses = db.relationship('DoubtResponse', backref='doubt', lazy=True, cascade='all, delete-orphan')
    attachments = db.relationship('DoubtAttachment', backref='doubt', lazy=True, cascade='all, delete-orphan')
    
    # User relationships
    student = db.relationship('User', foreign_keys=[student_id], backref='doubts_asked')
    teacher = db.relationship('User', foreign_keys=[assigned_to], backref='doubts_assigned')
    
    def __repr__(self):
        return f'<Doubt {self.id}: {self.title}>'
    
    @property
    def response_count(self):
        """Get the number of responses to the doubt"""
        return len(self.responses)

class DoubtResponse(db.Model):
    """Model for responses to doubts"""
    __tablename__ = 'doubt_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    doubt_id = db.Column(db.Integer, db.ForeignKey('doubts.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # User info
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Is this the accepted answer?
    is_accepted = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='doubt_responses')
    attachments = db.relationship('DoubtResponseAttachment', backref='response', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<DoubtResponse {self.id}>'

class DoubtAttachment(db.Model):
    """Model for attachments to doubts"""
    __tablename__ = 'doubt_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    doubt_id = db.Column(db.Integer, db.ForeignKey('doubts.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))  # MIME type
    file_size = db.Column(db.Integer)  # Size in bytes
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DoubtAttachment {self.id}>'

class DoubtResponseAttachment(db.Model):
    """Model for attachments to doubt responses"""
    __tablename__ = 'doubt_response_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('doubt_responses.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))  # MIME type
    file_size = db.Column(db.Integer)  # Size in bytes
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DoubtResponseAttachment {self.id}>' 
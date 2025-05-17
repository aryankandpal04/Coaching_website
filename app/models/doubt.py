from datetime import datetime
from app import db

class Doubt(db.Model):
    """Model for student doubts"""
    __tablename__ = 'doubts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Integer, nullable=False)  # Class 6-12
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='pending')  # pending, assigned, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    # Optional fields
    attachment_url = db.Column(db.String(500))
    priority = db.Column(db.String(20), default='normal')  # low, normal, high
    tags = db.Column(db.String(200))  # Comma-separated tags
    
    # Relationships
    responses = db.relationship('DoubtResponse', backref='doubt', lazy=True, cascade='all, delete-orphan')
    
    # User relationships
    student = db.relationship('User', foreign_keys=[student_id], backref='doubts_asked')
    teacher = db.relationship('User', foreign_keys=[teacher_id], backref='doubts_assigned')
    
    def __init__(self, title, description, subject, grade, student_id, **kwargs):
        self.title = title
        self.description = description
        self.subject = subject
        self.grade = grade
        self.student_id = student_id
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<Doubt {self.title}>'

class DoubtResponse(db.Model):
    """Model for responses to doubts"""
    __tablename__ = 'doubt_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    doubt_id = db.Column(db.Integer, db.ForeignKey('doubts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    attachment_url = db.Column(db.String(500))
    is_solution = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='doubt_responses')
    
    def __init__(self, doubt_id, user_id, content, **kwargs):
        self.doubt_id = doubt_id
        self.user_id = user_id
        self.content = content
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<DoubtResponse {self.id}>'

class DoubtAttachment(db.Model):
    """Model for attachments to doubts"""
    __tablename__ = 'doubt_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    doubt_id = db.Column(db.Integer, db.ForeignKey('doubts.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))  # MIME type
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DoubtAttachment {self.id}>'

class DoubtResponseAttachment(db.Model):
    """Model for attachments to doubt responses"""
    __tablename__ = 'doubt_response_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('doubt_responses.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))  # MIME type
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DoubtResponseAttachment {self.id}>' 
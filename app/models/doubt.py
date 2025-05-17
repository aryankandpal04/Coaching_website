from datetime import datetime
from app import db

class Doubt(db.Model):
    """Model for student doubts"""
    __tablename__ = 'doubts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Subject and grade
    subject = db.Column(db.String(100), nullable=False)
    class_level = db.Column(db.String(20), nullable=False)  # Class/Grade level
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, answered, resolved
    
    # User info
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Teacher assigned to answer
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    responses = db.relationship('DoubtResponse', backref='doubt', lazy='dynamic')
    attachments = db.relationship('DoubtAttachment', backref='doubt', lazy='dynamic')
    
    # User relationships
    student = db.relationship('User', foreign_keys=[student_id], backref='doubts_asked')
    teacher = db.relationship('User', foreign_keys=[teacher_id], backref='doubts_assigned')
    
    def __init__(self, title, content, subject, class_level, student_id):
        self.title = title
        self.content = content
        self.subject = subject
        self.class_level = class_level
        self.student_id = student_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'subject': self.subject,
            'class_level': self.class_level,
            'status': self.status,
            'student_id': self.student_id,
            'teacher_id': self.teacher_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
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
    attachments = db.relationship('DoubtResponseAttachment', backref='response', lazy='dynamic')
    
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
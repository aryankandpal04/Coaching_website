from datetime import datetime
from app import db

class Course(db.Model):
    """Model for courses"""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(20), nullable=False)  # Class/Grade level
    
    # Creator info
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    lectures = db.relationship('Lecture', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.title}>'
    
    @property
    def lecture_count(self):
        """Get the number of lectures in the course"""
        return len(self.lectures)

class Lecture(db.Model):
    """Model for lectures"""
    __tablename__ = 'lectures'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Content
    content_type = db.Column(db.String(20), nullable=False)  # 'video', 'document', 'presentation'
    content_url = db.Column(db.String(255))  # URL or file path
    
    # For videos
    video_duration = db.Column(db.Integer)  # Duration in seconds
    
    # Ordering
    order = db.Column(db.Integer, default=0)
    
    # Creator info
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    attachments = db.relationship('LectureAttachment', backref='lecture', lazy=True, cascade='all, delete-orphan')
    views = db.relationship('LectureView', backref='lecture', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Lecture {self.title}>'

class LectureAttachment(db.Model):
    """Model for lecture attachments"""
    __tablename__ = 'lecture_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))  # MIME type
    file_size = db.Column(db.Integer)  # Size in bytes
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LectureAttachment {self.title}>'

class LectureView(db.Model):
    """Model for tracking lecture views"""
    __tablename__ = 'lecture_views'
    
    id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # View details
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    watch_duration = db.Column(db.Integer)  # Duration watched in seconds
    
    def __repr__(self):
        return f'<LectureView {self.id}>' 
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
    __tablename__ = 'lectures'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    subject = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Integer, nullable=False)  # Class 6-12
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    video_url = db.Column(db.String(500))
    document_url = db.Column(db.String(500))
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Metadata
    duration = db.Column(db.Integer)  # Duration in minutes
    difficulty_level = db.Column(db.String(20))  # beginner, intermediate, advanced
    tags = db.Column(db.String(200))  # Comma-separated tags
    
    # Relationships
    comments = db.relationship('LectureComment', backref='lecture', lazy=True, cascade='all, delete-orphan')
    views = db.relationship('LectureView', backref='lecture', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, title, subject, grade, author_id, **kwargs):
        self.title = title
        self.subject = subject
        self.grade = grade
        self.author_id = author_id
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<Lecture {self.title}>'

class LectureComment(db.Model):
    __tablename__ = 'lecture_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='lecture_comments')

class LectureView(db.Model):
    __tablename__ = 'lecture_views'
    
    id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    watch_duration = db.Column(db.Integer)  # Duration watched in seconds
    completed = db.Column(db.Boolean, default=False)
    
    # Relationship
    user = db.relationship('User', backref='lecture_views')

    def __repr__(self):
        return f'<LectureView {self.id}>' 
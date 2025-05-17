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
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(500))
    subject = db.Column(db.String(100), nullable=False)
    class_level = db.Column(db.String(20), nullable=False)  # e.g., "6", "7", "8"
    duration = db.Column(db.Integer)  # in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    comments = db.relationship('LectureComment', backref='lecture', lazy='dynamic')
    bookmarks = db.relationship('LectureBookmark', backref='lecture', lazy='dynamic')
    views = db.relationship('LectureView', backref='lecture', lazy='dynamic')
    
    def __init__(self, title, description, subject, class_level, teacher_id):
        self.title = title
        self.description = description
        self.subject = subject
        self.class_level = class_level
        self.teacher_id = teacher_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'video_url': self.video_url,
            'subject': self.subject,
            'class_level': self.class_level,
            'duration': self.duration,
            'teacher_id': self.teacher_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Lecture {self.title}>'

class LectureComment(db.Model):
    """Model for lecture comments"""
    __tablename__ = 'lecture_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship
    user = db.relationship('User', backref='lecture_comments')

class LectureBookmark(db.Model):
    """Model for lecture bookmarks"""
    __tablename__ = 'lecture_bookmarks'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)  # timestamp in seconds
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship
    user = db.relationship('User', backref='lecture_bookmarks')

class LectureView(db.Model):
    """Model for tracking lecture views"""
    __tablename__ = 'lecture_views'
    
    id = db.Column(db.Integer, primary_key=True)
    view_date = db.Column(db.DateTime, default=datetime.utcnow)
    watch_duration = db.Column(db.Integer)  # duration watched in seconds
    
    # Foreign Keys
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship
    user = db.relationship('User', backref='lecture_views')

    def __repr__(self):
        return f'<LectureView {self.id}>' 
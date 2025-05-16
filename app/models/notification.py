from datetime import datetime
from app import db

class Notification(db.Model):
    """Model for user notifications"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Notification details
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # 'info', 'warning', 'success', 'error'
    
    # Status
    is_read = db.Column(db.Boolean, default=False)
    
    # Related entities
    related_model = db.Column(db.String(50))  # 'fee', 'doubt', 'test', 'lecture', etc.
    related_id = db.Column(db.Integer)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    
    def __repr__(self):
        return f'<Notification {self.id}: {self.title}>'
    
    def mark_as_read(self):
        """Mark the notification as read"""
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.commit()

class Announcement(db.Model):
    """Model for announcements"""
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Announcement details
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Target audience
    target_role = db.Column(db.String(50))  # 'all', 'admin', 'teacher', 'student', 'parent'
    target_grade = db.Column(db.String(20))  # For targeting specific grades
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Creator info
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    # Relationships
    creator = db.relationship('User', backref='announcements')
    
    def __repr__(self):
        return f'<Announcement {self.id}: {self.title}>'
    
    @property
    def is_expired(self):
        """Check if the announcement is expired"""
        if self.expires_at:
            return datetime.utcnow() > self.expires_at
        return False 
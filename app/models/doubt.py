from datetime import datetime
from app import db, cache
from typing import Dict, List, Optional
from app.models.notification import Notification
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
import firebase_admin
from firebase_admin import messaging

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
    student = db.relationship('User', foreign_keys=[student_id], back_populates='student_doubts')
    teacher = db.relationship('User', foreign_keys=[teacher_id], back_populates='teacher_doubts')
    
    def __init__(self, title, description, subject, grade, student_id, **kwargs):
        self.title = title
        self.description = description
        self.subject = subject
        self.grade = grade
        self.student_id = student_id
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def assign_teacher(self, teacher_id: int) -> bool:
        """Assign a teacher to the doubt"""
        try:
            self.teacher_id = teacher_id
            self.status = 'assigned'
            self.updated_at = datetime.utcnow()
            
            # Create notification for student
            Notification.create(
                user_id=self.student_id,
                title='Teacher Assigned',
                message=f'A teacher has been assigned to your doubt: {self.title}',
                notification_type='doubt_assigned',
                reference_id=self.id
            )
            
            # Send push notification
            self._send_push_notification(
                user_id=self.student_id,
                title='Teacher Assigned',
                body=f'A teacher has been assigned to your doubt: {self.title}'
            )
            
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    def mark_resolved(self, resolution_response: Optional[str] = None) -> bool:
        """Mark the doubt as resolved"""
        try:
            self.status = 'resolved'
            self.resolved_at = datetime.utcnow()
            
            if resolution_response:
                response = DoubtResponse(
                    doubt_id=self.id,
                    user_id=self.teacher_id,
                    content=resolution_response,
                    is_solution=True
                )
                db.session.add(response)
            
            # Create notification for student
            Notification.create(
                user_id=self.student_id,
                title='Doubt Resolved',
                message=f'Your doubt has been resolved: {self.title}',
                notification_type='doubt_resolved',
                reference_id=self.id
            )
            
            # Send push notification
            self._send_push_notification(
                user_id=self.student_id,
                title='Doubt Resolved',
                body=f'Your doubt has been resolved: {self.title}'
            )
            
            # Clear cache
            cache.delete(f'doubt_{self.id}')
            cache.delete(f'student_doubts_{self.student_id}')
            
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    def add_response(self, user_id: int, content: str, attachment_url: Optional[str] = None) -> Optional['DoubtResponse']:
        """Add a response to the doubt"""
        try:
            response = DoubtResponse(
                doubt_id=self.id,
                user_id=user_id,
                content=content,
                attachment_url=attachment_url
            )
            db.session.add(response)
            
            # Create notification for relevant users
            notify_user_id = self.student_id if user_id == self.teacher_id else self.teacher_id
            Notification.create(
                user_id=notify_user_id,
                title='New Response',
                message=f'New response added to doubt: {self.title}',
                notification_type='doubt_response',
                reference_id=self.id
            )
            
            # Send push notification
            self._send_push_notification(
                user_id=notify_user_id,
                title='New Response',
                body=f'New response added to doubt: {self.title}'
            )
            
            # Clear cache
            cache.delete(f'doubt_{self.id}')
            
            db.session.commit()
            return response
        except SQLAlchemyError:
            db.session.rollback()
            return None
    
    def get_timeline(self) -> List[Dict]:
        """Get timeline of doubt activities"""
        timeline = []
        
        # Add creation event
        timeline.append({
            'type': 'created',
            'timestamp': self.created_at,
            'user_id': self.student_id,
            'content': self.description
        })
        
        # Add assignment event if applicable
        if self.teacher_id:
            timeline.append({
                'type': 'assigned',
                'timestamp': self.updated_at,
                'user_id': self.teacher_id,
                'content': None
            })
        
        # Add responses
        responses = self.responses.all()
        for response in responses:
            timeline.append({
                'type': 'response',
                'timestamp': response.created_at,
                'user_id': response.user_id,
                'content': response.content,
                'is_solution': response.is_solution
            })
        
        # Add resolution event if applicable
        if self.resolved_at:
            timeline.append({
                'type': 'resolved',
                'timestamp': self.resolved_at,
                'user_id': self.teacher_id,
                'content': None
            })
        
        return sorted(timeline, key=lambda x: x['timestamp'])
    
    @staticmethod
    def _send_push_notification(user_id: int, title: str, body: str) -> bool:
        """Send push notification using Firebase"""
        try:
            # Get user's FCM token from your user model
            from app.models.user import User
            user = User.query.get(user_id)
            if not user or not user.fcm_token:
                return False
            
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                token=user.fcm_token
            )
            
            messaging.send(message)
            return True
        except Exception as e:
            current_app.logger.error(f"Error sending push notification: {str(e)}")
            return False
    
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

    def mark_as_solution(self) -> bool:
        """Mark this response as the solution"""
        try:
            # Unmark any existing solution
            DoubtResponse.query.filter_by(
                doubt_id=self.doubt_id,
                is_solution=True
            ).update({'is_solution': False})
            
            self.is_solution = True
            self.doubt.mark_resolved()
            
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    def edit_response(self, new_content: str) -> bool:
        """Edit the response content"""
        try:
            self.content = new_content
            self.updated_at = datetime.utcnow()
            
            # Clear cache
            cache.delete(f'doubt_{self.doubt_id}')
            
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

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
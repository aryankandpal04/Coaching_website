from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# Association table for user-role relationship
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

class Role(db.Model):
    """Role model for defining user permissions"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Role {self.name}>'

class User(UserMixin, db.Model):
    """User model for authentication and role-based permissions"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    active = db.Column(db.Boolean, default=True)
    
    # Profile info
    profile_image = db.Column(db.String(255))  # Path to profile image
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = db.Column(db.DateTime)
    
    # Relations
    roles = db.relationship('Role', secondary=user_roles, lazy='subquery',
                           backref=db.backref('users', lazy=True))
    
    # Class-specific fields (based on role)
    grade = db.Column(db.String(20))  # For students
    subjects = db.Column(db.Text)  # For teachers, comma-separated list of subjects
    
    # Parent-student relationship
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    children = db.relationship('User', backref=db.backref('parent', remote_side=[id]), lazy=True)
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the user's password"""
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role_name):
        """Check if the user has the specified role"""
        return any(role.name == role_name for role in self.roles)
    
    @property
    def full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_admin(self):
        """Check if the user is an admin"""
        return self.has_role('admin')
    
    @property
    def is_teacher(self):
        """Check if the user is a teacher"""
        return self.has_role('teacher')
    
    @property
    def is_student(self):
        """Check if the user is a student"""
        return self.has_role('student')
    
    @property
    def is_parent(self):
        """Check if the user is a parent"""
        return self.has_role('parent') 
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

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
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student, parent
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Role-specific fields
    # For students
    grade = db.Column(db.Integer)  # Class 6-12
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # For teachers
    subjects = db.Column(db.String(255))  # Comma-separated list of subjects
    qualifications = db.Column(db.String(255))
    
    # Profile info
    profile_image = db.Column(db.String(255))  # Path to profile image
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    
    # Timestamps
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = db.Column(db.DateTime)
    
    # Relations
    roles = db.relationship('Role', secondary=user_roles, lazy='subquery',
                           backref=db.backref('users', lazy=True))
    
    # Relationships
    students = db.relationship('User', backref=db.backref('parent', remote_side=[id]),
                             foreign_keys='User.parent_id')
    lectures = db.relationship('Lecture', backref='author', lazy=True)
    doubts_created = db.relationship('Doubt', 
                                   foreign_keys='Doubt.student_id',
                                   back_populates='student',
                                   overlaps="student_doubts")
    doubts_assigned = db.relationship('Doubt',
                                    foreign_keys='Doubt.teacher_id',
                                    back_populates='teacher',
                                    overlaps="teacher_doubts")
    student_doubts = db.relationship('Doubt',
                                   foreign_keys='Doubt.student_id',
                                   back_populates='student',
                                   overlaps="doubts_created")
    teacher_doubts = db.relationship('Doubt',
                                   foreign_keys='Doubt.teacher_id',
                                   back_populates='teacher',
                                   overlaps="doubts_assigned")
    test_results = db.relationship('TestResult', backref='student', lazy=True)
    fees = db.relationship('Fee', backref='student', lazy='dynamic')
    
    def __init__(self, email, username, role, **kwargs):
        self.email = email
        self.username = username
        self.role = role
        for key, value in kwargs.items():
            setattr(self, key, value)
    
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
        return role_name == self.role
    
    @property
    def full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_admin(self):
        """Check if the user is an admin"""
        return self.role == 'admin'
    
    @property
    def is_teacher(self):
        """Check if the user is a teacher"""
        return self.role == 'teacher'
    
    @property
    def is_student(self):
        """Check if the user is a student"""
        return self.role == 'student'
    
    @property
    def is_parent(self):
        """Check if the user is a parent"""
        return self.role == 'parent'
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 
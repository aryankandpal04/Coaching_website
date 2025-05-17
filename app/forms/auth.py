from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
import re
from app.models.user import User

class LoginForm(FlaskForm):
    """Form for user login"""
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    """Form for user registration"""
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=50),
        Regexp(r'^[A-Za-z\s-]+$', message="First name can only contain letters, spaces, and hyphens")
    ])
    
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=50),
        Regexp(r'^[A-Za-z\s-]+$', message="Last name can only contain letters, spaces, and hyphens")
    ])
    
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=30),
        Regexp(r'^[A-Za-z0-9_-]+$', message="Username can only contain letters, numbers, underscores, and hyphens")
    ])
    
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Please enter a valid email address"),
        Length(max=120)
    ])
    
    role = SelectField('I am a', choices=[
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent')
    ], validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long"),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]',
               message="Password must contain at least one letter, one number, and one special character")
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Policy', validators=[
        DataRequired(message="You must accept the Terms of Service and Privacy Policy to register")
    ])
    
    submit = SubmitField('Create Account')
    
    def validate_email(self, field):
        """Validate that the email is unique"""
        user = User.query.filter_by(email=field.data.lower()).first()
        if user is not None:
            raise ValidationError('Email address is already registered')
    
    def validate_username(self, field):
        """Validate that the username is unique"""
        user = User.query.filter_by(username=field.data.lower()).first()
        if user is not None:
            raise ValidationError('Username is already taken')

class ForgotPasswordForm(FlaskForm):
    """Form for requesting password reset"""
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Please enter a valid email address")
    ])
    submit = SubmitField('Reset Password')

class ResetPasswordForm(FlaskForm):
    """Form for resetting password"""
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long"),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]',
               message="Password must contain at least one letter, one number, and one special character")
    ])
    
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    
    submit = SubmitField('Reset Password') 
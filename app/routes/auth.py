from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from datetime import datetime
import os
from werkzeug.utils import secure_filename

from app import db
from app.models.user import User, Role
from app.forms.auth import LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm
from app.utils.jwt import generate_token, verify_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            
            # Generate tokens
            access_token = generate_token(user, 'access')
            refresh_token = generate_token(user, 'refresh')
            
            # Store tokens in session
            session['access_token'] = access_token
            session['refresh_token'] = refresh_token
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('teacher.dashboard'))
            elif user.role == 'student':
                return redirect(url_for('student.dashboard'))
            elif user.role == 'parent':
                return redirect(url_for('parent.dashboard'))
            
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Invalid email or password', 'error')
    
    return render_template('auth/login.html', title='Sign In', form=form)

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    """API login endpoint"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
        
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = generate_token(user, 'access')
        refresh_token = generate_token(user, 'refresh')
        
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
    
    return jsonify({'error': 'Invalid email or password'}), 401

@auth_bp.route('/api/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token using refresh token"""
    refresh_token = request.headers.get('Authorization')
    if not refresh_token:
        return jsonify({'error': 'Refresh token required'}), 401
    
    payload = verify_token(refresh_token.replace('Bearer ', ''))
    if not payload or payload['type'] != 'refresh':
        return jsonify({'error': 'Invalid refresh token'}), 401
    
    user = User.query.get(payload['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    new_access_token = generate_token(user, 'access')
    return jsonify({'access_token': new_access_token})

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout route"""
    logout_user()
    session.pop('access_token', None)
    session.pop('refresh_token', None)
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(
            email=form.email.data,
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role=form.role.data,
            grade=form.grade.data if form.role.data == 'student' else None
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        
        if user:
            # Generate password reset token and send email
            # Implementation will be added later
            flash('If your email is registered, you will receive a password reset link shortly.', 'info')
        else:
            # Still show the same message for security reasons
            flash('If your email is registered, you will receive a password reset link shortly.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html', title='Forgot Password', form=form)

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    # Verify token and get user
    # Implementation will be added later
    user = None  # Placeholder
    
    if not user:
        flash('Invalid or expired password reset link', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', title='Reset Password', form=form)

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile route"""
    if request.method == 'POST':
        # Update profile information
        current_user.first_name = request.form.get('first_name', current_user.first_name)
        current_user.last_name = request.form.get('last_name', current_user.last_name)
        current_user.phone = request.form.get('phone', current_user.phone)
        
        if current_user.is_student:
            current_user.grade = request.form.get('grade', current_user.grade, type=int)
        elif current_user.is_teacher:
            current_user.subjects = request.form.get('subjects', current_user.subjects)
            current_user.qualifications = request.form.get('qualifications', current_user.qualifications)
        
        # Handle profile image upload
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                current_user.profile_image = filename
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html', title='My Profile', user=current_user)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
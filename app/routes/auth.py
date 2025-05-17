from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from app import db
from app.models.user import User, Role
from app.forms.auth import LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return render_template('auth/login.html', form=form)
        
        if not user.active:
            flash('Your account has been deactivated. Please contact support.', 'warning')
            return render_template('auth/login.html', form=form)
        
        # Log the user in
        login_user(user, remember=form.remember_me.data)
        
        # Update last login timestamp
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        
        # Redirect to requested page or dashboard
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        
        return redirect(next_page)
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    """User logout route"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                email=form.email.data.lower(),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                grade=form.grade.data if form.role.data == 'student' else None
            )
            user.set_password(form.password.data)
            
            # Assign role
            role = Role.query.filter_by(name=form.role.data).first()
            if role:
                user.roles.append(role)
            else:
                flash('Invalid role selected', 'danger')
                return render_template('auth/register.html', form=form)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed. Please try again.', 'danger')
            return render_template('auth/register.html', form=form)
    
    # If form validation failed, print the errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
    
    return render_template('auth/register.html', form=form)

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
    
    return render_template('auth/forgot_password.html', form=form)

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
    
    return render_template('auth/reset_password.html', form=form) 
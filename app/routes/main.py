from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage route"""
    return render_template('main/index.html')

@main_bp.route('/about')
def about():
    """About page route"""
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    """Contact page route"""
    return render_template('main/contact.html')

@main_bp.route('/features')
def features():
    """Features page route"""
    return render_template('main/features.html')

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard redirect based on user role"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Redirect based on user role
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    elif current_user.is_teacher:
        return redirect(url_for('teacher.dashboard'))
    elif current_user.is_student:
        return redirect(url_for('student.dashboard'))
    elif current_user.is_parent:
        return redirect(url_for('parent.dashboard'))
    
    # Default fallback
    return redirect(url_for('main.index')) 
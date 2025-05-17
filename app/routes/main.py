from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import current_user, login_required

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
@login_required
def dashboard():
    if current_user.is_admin():
        return render_template('admin/dashboard.html')
    elif current_user.is_teacher():
        return render_template('teacher/dashboard.html')
    elif current_user.is_student():
        return render_template('student/dashboard.html')
    elif current_user.is_parent():
        return render_template('parent/dashboard.html')
    return render_template('main/dashboard.html') 
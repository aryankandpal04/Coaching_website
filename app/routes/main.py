from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import current_user, login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage route - Landing page for non-authenticated users"""
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
        elif current_user.role == 'parent':
            return redirect(url_for('parent.dashboard'))
    
    return render_template('main/index.html')

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('main/contact.html')

@main_bp.route('/features')
def features():
    """Features page"""
    return render_template('main/features.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard route that redirects to role-specific dashboards"""
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    elif current_user.is_teacher:
        return redirect(url_for('teacher.dashboard'))
    elif current_user.is_student:
        return redirect(url_for('student.dashboard'))
    elif current_user.is_parent:
        return redirect(url_for('parent.dashboard'))
    return render_template('main/dashboard.html') 
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    """
    Decorator for routes that require admin access
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    """
    Decorator for routes that require teacher access
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_teacher:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    """
    Decorator for routes that require student access
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_student:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def parent_required(f):
    """
    Decorator for routes that require parent access
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_parent:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function 
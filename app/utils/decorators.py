from functools import wraps
from flask import flash, redirect, url_for, request, jsonify
from flask_login import current_user
from app.utils.jwt import verify_token

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

def jwt_required(f):
    """Decorator for API routes that require JWT token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Missing authorization header'}), 401
        
        token = auth_header.replace('Bearer ', '')
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator for routes that require specific roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                flash(f'Access denied. {", ".join(roles)} privileges required.', 'error')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def api_role_required(*roles):
    """Decorator for API routes that require specific roles"""
    def decorator(f):
        @wraps(f)
        @jwt_required
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({'error': 'Missing authorization header'}), 401
            
            token = auth_header.replace('Bearer ', '')
            payload = verify_token(token)
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            if payload.get('role') not in roles:
                return jsonify({'error': f'Access denied. {", ".join(roles)} privileges required.'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

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
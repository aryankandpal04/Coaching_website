from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app.models.user import User
from app.models.lecture import Lecture
from app.models.test import Test
from app.models.doubt import Doubt
from app.models.fee import Fee
from app import db

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to check if current user is an admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    users = User.query.count()
    lectures = Lecture.query.count()
    tests = Test.query.count()
    doubts = Doubt.query.count()
    pending_fees = Fee.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html',
                         users=users,
                         lectures=lectures,
                         tests=tests,
                         doubts=doubts,
                         pending_fees=pending_fees)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    flash(f'User status updated successfully', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/lectures')
@login_required
@admin_required
def lectures():
    page = request.args.get('page', 1, type=int)
    lectures = Lecture.query.paginate(page=page, per_page=20)
    return render_template('admin/lectures.html', lectures=lectures)

@admin_bp.route('/tests')
@login_required
@admin_required
def tests():
    page = request.args.get('page', 1, type=int)
    tests = Test.query.paginate(page=page, per_page=20)
    return render_template('admin/tests.html', tests=tests)

@admin_bp.route('/doubts')
@login_required
@admin_required
def doubts():
    page = request.args.get('page', 1, type=int)
    doubts = Doubt.query.paginate(page=page, per_page=20)
    return render_template('admin/doubts.html', doubts=doubts)

@admin_bp.route('/fees')
@login_required
@admin_required
def fees():
    page = request.args.get('page', 1, type=int)
    fees = Fee.query.paginate(page=page, per_page=20)
    return render_template('admin/fees.html', fees=fees)

@admin_bp.route('/payments')
@login_required
@admin_required
def payments():
    """Payment management route"""
    return render_template('admin/payments.html')

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    """Reports route"""
    return render_template('admin/reports.html') 
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard route"""
    return render_template('admin/dashboard.html')

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """User management route"""
    return render_template('admin/users.html')

@admin_bp.route('/tests')
@login_required
@admin_required
def tests():
    """Test management route"""
    return render_template('admin/tests.html')

@admin_bp.route('/lectures')
@login_required
@admin_required
def lectures():
    """Lecture management route"""
    return render_template('admin/lectures.html')

@admin_bp.route('/doubts')
@login_required
@admin_required
def doubts():
    """Doubt management route"""
    return render_template('admin/doubts.html')

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
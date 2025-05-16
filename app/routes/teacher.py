from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.utils.decorators import teacher_required

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    """Teacher dashboard route"""
    return render_template('teacher/dashboard.html')

@teacher_bp.route('/lectures')
@login_required
@teacher_required
def lectures():
    """Teacher lectures management route"""
    return render_template('teacher/lectures.html')

@teacher_bp.route('/tests')
@login_required
@teacher_required
def tests():
    """Teacher tests management route"""
    return render_template('teacher/tests.html')

@teacher_bp.route('/doubts')
@login_required
@teacher_required
def doubts():
    """Teacher doubts management route"""
    return render_template('teacher/doubts.html')

@teacher_bp.route('/students')
@login_required
@teacher_required
def students():
    """Teacher students view route"""
    return render_template('teacher/students.html')

@teacher_bp.route('/reports')
@login_required
@teacher_required
def reports():
    """Teacher reports route"""
    return render_template('teacher/reports.html') 
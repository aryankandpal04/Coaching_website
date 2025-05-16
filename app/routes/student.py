from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.utils.decorators import student_required

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    """Student dashboard route"""
    return render_template('student/dashboard.html')

@student_bp.route('/lectures')
@login_required
@student_required
def lectures():
    """Student lectures view route"""
    return render_template('student/lectures.html')

@student_bp.route('/tests')
@login_required
@student_required
def tests():
    """Student tests list route"""
    return render_template('student/tests.html')

@student_bp.route('/tests/<int:test_id>')
@login_required
@student_required
def take_test(test_id):
    """Student take test route"""
    return render_template('student/take_test.html', test_id=test_id)

@student_bp.route('/doubts')
@login_required
@student_required
def doubts():
    """Student doubts route"""
    return render_template('student/doubts.html')

@student_bp.route('/doubts/new')
@login_required
@student_required
def new_doubt():
    """Student new doubt route"""
    return render_template('student/new_doubt.html')

@student_bp.route('/performance')
@login_required
@student_required
def performance():
    """Student performance route"""
    return render_template('student/performance.html')

@student_bp.route('/fees')
@login_required
@student_required
def fees():
    """Student fees route"""
    return render_template('student/fees.html') 
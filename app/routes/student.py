from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app.models.lecture import Lecture, LectureView
from app.models.test import Test, TestResult
from app.models.doubt import Doubt
from app.models.fee import Fee
from app import db

student_bp = Blueprint('student', __name__)

def student_required(f):
    """Decorator to check if current user is a student"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_student:
            flash('Access denied. Student privileges required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    """Student dashboard showing their statistics"""
    lectures_viewed = LectureView.query.filter_by(user_id=current_user.id).count()
    tests_taken = TestResult.query.filter_by(student_id=current_user.id).count()
    pending_doubts = Doubt.query.filter_by(student_id=current_user.id, status='pending').count()
    pending_fees = Fee.query.filter_by(student_id=current_user.id, status='pending').count()
    
    return render_template('student/dashboard.html',
                         lectures_viewed=lectures_viewed,
                         tests_taken=tests_taken,
                         pending_doubts=pending_doubts,
                         pending_fees=pending_fees)

@student_bp.route('/lectures')
@login_required
@student_required
def lectures():
    page = request.args.get('page', 1, type=int)
    lectures = Lecture.query.filter_by(grade=current_user.grade, is_published=True)\
        .paginate(page=page, per_page=20)
    return render_template('student/lectures.html', lectures=lectures)

@student_bp.route('/lectures/<int:lecture_id>')
@login_required
@student_required
def view_lecture(lecture_id):
    lecture = Lecture.query.get_or_404(lecture_id)
    
    # Record lecture view
    view = LectureView(
        lecture_id=lecture.id,
        user_id=current_user.id
    )
    db.session.add(view)
    db.session.commit()
    
    return render_template('student/view_lecture.html', lecture=lecture)

@student_bp.route('/tests')
@login_required
@student_required
def tests():
    page = request.args.get('page', 1, type=int)
    tests = Test.query.filter_by(grade=current_user.grade, is_published=True)\
        .paginate(page=page, per_page=20)
    return render_template('student/tests.html', tests=tests)

@student_bp.route('/tests/<int:test_id>')
@login_required
@student_required
def take_test(test_id):
    test = Test.query.get_or_404(test_id)
    
    # Check if test is already taken
    result = TestResult.query.filter_by(
        test_id=test.id,
        student_id=current_user.id,
        status='completed'
    ).first()
    
    if result and not test.allow_retake:
        flash('You have already taken this test', 'error')
        return redirect(url_for('student.tests'))
    
    return render_template('student/take_test.html', test=test)

@student_bp.route('/doubts')
@login_required
@student_required
def doubts():
    page = request.args.get('page', 1, type=int)
    doubts = Doubt.query.filter_by(student_id=current_user.id)\
        .paginate(page=page, per_page=20)
    return render_template('student/doubts.html', doubts=doubts)

@student_bp.route('/doubts/create', methods=['GET', 'POST'])
@login_required
@student_required
def create_doubt():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        subject = request.form.get('subject')
        
        doubt = Doubt(
            title=title,
            description=description,
            subject=subject,
            grade=current_user.grade,
            student_id=current_user.id
        )
        db.session.add(doubt)
        db.session.commit()
        
        flash('Doubt posted successfully', 'success')
        return redirect(url_for('student.doubts'))
    
    return render_template('student/create_doubt.html')

@student_bp.route('/fees')
@login_required
@student_required
def fees():
    page = request.args.get('page', 1, type=int)
    fees = Fee.query.filter_by(student_id=current_user.id)\
        .paginate(page=page, per_page=20)
    return render_template('student/fees.html', fees=fees) 
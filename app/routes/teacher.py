from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.lecture import Lecture
from app.models.test import Test
from app.models.doubt import Doubt
from app import db

teacher_bp = Blueprint('teacher', __name__)

def teacher_required(f):
    """Decorator to check if current user is a teacher"""
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_teacher():
            flash('Access denied. Teacher privileges required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    lectures = Lecture.query.filter_by(author_id=current_user.id).count()
    tests = Test.query.filter_by(creator_id=current_user.id).count()
    pending_doubts = Doubt.query.filter_by(teacher_id=current_user.id, status='pending').count()
    
    return render_template('teacher/dashboard.html',
                         lectures=lectures,
                         tests=tests,
                         pending_doubts=pending_doubts)

@teacher_bp.route('/lectures')
@login_required
@teacher_required
def lectures():
    page = request.args.get('page', 1, type=int)
    lectures = Lecture.query.filter_by(author_id=current_user.id)\
        .paginate(page=page, per_page=20)
    return render_template('teacher/lectures.html', lectures=lectures)

@teacher_bp.route('/lectures/create', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_lecture():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        subject = request.form.get('subject')
        grade = request.form.get('grade')
        content = request.form.get('content')
        
        lecture = Lecture(
            title=title,
            description=description,
            subject=subject,
            grade=grade,
            content=content,
            author_id=current_user.id
        )
        db.session.add(lecture)
        db.session.commit()
        
        flash('Lecture created successfully', 'success')
        return redirect(url_for('teacher.lectures'))
    
    return render_template('teacher/create_lecture.html')

@teacher_bp.route('/tests')
@login_required
@teacher_required
def tests():
    page = request.args.get('page', 1, type=int)
    tests = Test.query.filter_by(creator_id=current_user.id)\
        .paginate(page=page, per_page=20)
    return render_template('teacher/tests.html', tests=tests)

@teacher_bp.route('/tests/create', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_test():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        subject = request.form.get('subject')
        grade = request.form.get('grade')
        duration = request.form.get('duration')
        total_marks = request.form.get('total_marks')
        passing_marks = request.form.get('passing_marks')
        
        test = Test(
            title=title,
            description=description,
            subject=subject,
            grade=grade,
            duration=duration,
            total_marks=total_marks,
            passing_marks=passing_marks,
            creator_id=current_user.id
        )
        db.session.add(test)
        db.session.commit()
        
        flash('Test created successfully', 'success')
        return redirect(url_for('teacher.tests'))
    
    return render_template('teacher/create_test.html')

@teacher_bp.route('/doubts')
@login_required
@teacher_required
def doubts():
    page = request.args.get('page', 1, type=int)
    doubts = Doubt.query.filter_by(teacher_id=current_user.id)\
        .paginate(page=page, per_page=20)
    return render_template('teacher/doubts.html', doubts=doubts)

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
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app.models.user import User
from app.models.test import TestResult
from app.models.fee import Fee, Payment
from app import db

parent_bp = Blueprint('parent', __name__)

def parent_required(f):
    """Decorator to check if current user is a parent"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_parent():
            flash('Access denied. Parent privileges required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@parent_bp.route('/dashboard')
@login_required
@parent_required
def dashboard():
    # Get children's information
    children = User.query.filter_by(parent_id=current_user.id).all()
    
    # Get pending fees for all children
    pending_fees = 0
    for child in children:
        pending_fees += Fee.query.filter_by(student_id=child.id, status='pending').count()
    
    return render_template('parent/dashboard.html',
                         children=children,
                         pending_fees=pending_fees)

@parent_bp.route('/children')
@login_required
@parent_required
def children():
    children = User.query.filter_by(parent_id=current_user.id).all()
    return render_template('parent/children.html', children=children)

@parent_bp.route('/children/<int:child_id>/performance')
@login_required
@parent_required
def child_performance(child_id):
    child = User.query.get_or_404(child_id)
    
    # Verify the child belongs to the parent
    if child.parent_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('parent.children'))
    
    # Get test results
    test_results = TestResult.query.filter_by(student_id=child.id)\
        .order_by(TestResult.created_at.desc()).all()
    
    return render_template('parent/child_performance.html',
                         child=child,
                         test_results=test_results)

@parent_bp.route('/children/<int:child_id>/tests')
@login_required
@parent_required
def child_tests(child_id):
    """Parent child tests route"""
    return render_template('parent/child_tests.html', child_id=child_id)

@parent_bp.route('/fees')
@login_required
@parent_required
def fees():
    children = User.query.filter_by(parent_id=current_user.id).all()
    child_ids = [child.id for child in children]
    
    page = request.args.get('page', 1, type=int)
    fees = Fee.query.filter(Fee.student_id.in_(child_ids))\
        .paginate(page=page, per_page=20)
    
    return render_template('parent/fees.html', fees=fees)

@parent_bp.route('/payments')
@login_required
@parent_required
def payments():
    children = User.query.filter_by(parent_id=current_user.id).all()
    child_ids = [child.id for child in children]
    
    page = request.args.get('page', 1, type=int)
    fees = Fee.query.filter(Fee.student_id.in_(child_ids))\
        .filter_by(status='pending')\
        .paginate(page=page, per_page=20)
    
    return render_template('parent/payments.html', fees=fees)

@parent_bp.route('/payments/<int:fee_id>', methods=['POST'])
@login_required
@parent_required
def make_payment(fee_id):
    fee = Fee.query.get_or_404(fee_id)
    
    # Verify the fee belongs to one of the parent's children
    children = User.query.filter_by(parent_id=current_user.id).all()
    child_ids = [child.id for child in children]
    if fee.student_id not in child_ids:
        flash('Access denied', 'error')
        return redirect(url_for('parent.payments'))
    
    # Process payment (integrate with payment gateway)
    payment = Payment(
        fee_id=fee.id,
        amount=fee.amount,
        payment_method='online'
    )
    db.session.add(payment)
    
    fee.status = 'paid'
    fee.amount_paid = fee.amount
    fee.payment_method = 'online'
    
    db.session.commit()
    
    flash('Payment successful', 'success')
    return redirect(url_for('parent.payments')) 
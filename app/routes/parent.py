from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app.models.user import User
from app.models.test import TestResult
from app.models.fee import Fee, Payment
from app import db
from app.utils.decorators import role_required, api_role_required

parent_bp = Blueprint('parent', __name__)

def parent_required(f):
    """Decorator to check if current user is a parent"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_parent:
            flash('Access denied. Parent privileges required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@parent_bp.route('/dashboard')
@login_required
@role_required('parent')
def dashboard():
    """Parent dashboard"""
    children = User.query.filter_by(parent_id=current_user.id).all()
    children_data = []
    
    for child in children:
        test_results = TestResult.query.filter_by(student_id=child.id).all()
        avg_performance = sum(result.score for result in test_results) / len(test_results) if test_results else 0
        
        pending_fees = Fee.query.filter_by(student_id=child.id, status='pending').all()
        total_pending = sum(fee.amount for fee in pending_fees)
        
        children_data.append({
            'id': child.id,
            'name': f"{child.first_name} {child.last_name}",
            'grade': child.grade,
            'performance': avg_performance,
            'pending_fees': total_pending
        })
    
    return render_template('parent/dashboard.html',
                         children=children_data,
                         children_count=len(children_data))

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

@parent_bp.route('/api/children')
@api_role_required('parent')
def get_children():
    """API endpoint to get children data"""
    children = User.query.filter_by(parent_id=current_user.id).all()
    return jsonify([{
        'id': child.id,
        'name': f"{child.first_name} {child.last_name}",
        'grade': child.grade,
        'email': child.email
    } for child in children])

@parent_bp.route('/api/child/<int:child_id>/performance')
@api_role_required('parent')
def get_child_performance(child_id):
    """API endpoint to get child's performance data"""
    child = User.query.filter_by(id=child_id, parent_id=current_user.id).first_or_404()
    test_results = TestResult.query.filter_by(student_id=child.id).all()
    
    return jsonify([{
        'test_id': r.test_id,
        'score': r.score,
        'date': r.date.isoformat()
    } for r in test_results])

@parent_bp.route('/api/child/<int:child_id>/fees')
@api_role_required('parent')
def get_child_fees(child_id):
    """API endpoint to get child's fee data"""
    child = User.query.filter_by(id=child_id, parent_id=current_user.id).first_or_404()
    fees = Fee.query.filter_by(student_id=child.id).all()
    
    return jsonify([{
        'id': f.id,
        'amount': f.amount,
        'due_date': f.due_date.isoformat(),
        'status': f.status
    } for f in fees]) 
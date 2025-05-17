from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.user import User
from app.models.lecture import Lecture
from app.models.test import Test
from app.models.doubt import Doubt
from app.models.fee import Fee
from app import db, cache

api_bp = Blueprint('api', __name__)

@api_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """Get general statistics for dashboard."""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
        
    stats = cache.get('dashboard_stats')
    if stats is None:
        stats = {
            'total_users': User.query.count(),
            'total_lectures': Lecture.query.count(),
            'total_tests': Test.query.count(),
            'total_doubts': Doubt.query.count(),
            'pending_fees': Fee.query.filter_by(status='pending').count()
        }
        cache.set('dashboard_stats', stats, timeout=300)  # Cache for 5 minutes
    
    return jsonify(stats)

@api_bp.route('/user/<int:user_id>/progress', methods=['GET'])
@login_required
def get_user_progress(user_id):
    """Get learning progress for a specific user."""
    if not (current_user.id == user_id or current_user.is_admin or current_user.is_teacher):
        return jsonify({'error': 'Unauthorized'}), 403
        
    user = User.query.get_or_404(user_id)
    progress = {
        'completed_lectures': user.completed_lectures.count(),
        'test_scores': [{'test_id': score.test_id, 'score': score.score} 
                       for score in user.test_scores],
        'doubts_asked': user.doubts.count(),
        'doubts_resolved': user.doubts.filter_by(status='resolved').count()
    }
    
    return jsonify(progress)

@api_bp.route('/lectures/search', methods=['GET'])
@login_required
def search_lectures():
    """Search lectures by title or content."""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    lectures = Lecture.query.filter(
        (Lecture.title.ilike(f'%{query}%')) |
        (Lecture.content.ilike(f'%{query}%'))
    ).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'lectures': [{
            'id': lecture.id,
            'title': lecture.title,
            'subject': lecture.subject,
            'created_at': lecture.created_at.isoformat()
        } for lecture in lectures.items],
        'total': lectures.total,
        'pages': lectures.pages,
        'current_page': lectures.page
    })

@api_bp.route('/doubts/pending', methods=['GET'])
@login_required
def get_pending_doubts():
    """Get list of pending doubts for teachers."""
    if not (current_user.is_admin or current_user.is_teacher):
        return jsonify({'error': 'Unauthorized'}), 403
        
    doubts = Doubt.query.filter_by(status='pending').order_by(Doubt.created_at.desc()).all()
    return jsonify({
        'doubts': [{
            'id': doubt.id,
            'subject': doubt.subject,
            'question': doubt.question,
            'student_id': doubt.student_id,
            'created_at': doubt.created_at.isoformat()
        } for doubt in doubts]
    })

@api_bp.route('/fees/summary', methods=['GET'])
@login_required
def get_fee_summary():
    """Get fee payment summary for admin and parents."""
    if not (current_user.is_admin or current_user.is_parent):
        return jsonify({'error': 'Unauthorized'}), 403
        
    if current_user.is_parent:
        # Get fees for parent's children
        student_ids = [child.id for child in current_user.children]
        fees = Fee.query.filter(Fee.student_id.in_(student_ids)).all()
    else:
        # Admin sees all fees
        fees = Fee.query.all()
    
    summary = {
        'total_amount': sum(fee.amount for fee in fees),
        'paid_amount': sum(fee.amount for fee in fees if fee.status == 'paid'),
        'pending_amount': sum(fee.amount for fee in fees if fee.status == 'pending'),
        'recent_payments': [{
            'id': fee.id,
            'student_id': fee.student_id,
            'amount': fee.amount,
            'status': fee.status,
            'due_date': fee.due_date.isoformat()
        } for fee in fees[:5]]  # Last 5 payments
    }
    
    return jsonify(summary)
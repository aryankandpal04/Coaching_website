from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.utils.decorators import parent_required

parent_bp = Blueprint('parent', __name__)

@parent_bp.route('/dashboard')
@login_required
@parent_required
def dashboard():
    """Parent dashboard route"""
    return render_template('parent/dashboard.html')

@parent_bp.route('/children')
@login_required
@parent_required
def children():
    """Parent children list route"""
    return render_template('parent/children.html')

@parent_bp.route('/children/<int:child_id>/performance')
@login_required
@parent_required
def child_performance(child_id):
    """Parent child performance route"""
    return render_template('parent/child_performance.html', child_id=child_id)

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
    """Parent fees route"""
    return render_template('parent/fees.html')

@parent_bp.route('/messages')
@login_required
@parent_required
def messages():
    """Parent messages route"""
    return render_template('parent/messages.html') 
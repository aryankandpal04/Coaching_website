from datetime import datetime
from app import db

class Fee(db.Model):
    """Model for student fees"""
    __tablename__ = 'fees'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Fee details
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # 'pending', 'paid', 'overdue'
    
    # Fee type
    fee_type = db.Column(db.String(50), nullable=False)  # 'tuition', 'exam', 'material', etc.
    
    # Period
    period_start = db.Column(db.Date)
    period_end = db.Column(db.Date)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payments = db.relationship('Payment', backref='fee', lazy=True)
    student = db.relationship('User', backref='fees')
    
    def __repr__(self):
        return f'<Fee {self.id}: {self.title}>'
    
    @property
    def amount_paid(self):
        """Calculate the total amount paid for this fee"""
        return sum(payment.amount for payment in self.payments if payment.status == 'completed')
    
    @property
    def amount_due(self):
        """Calculate the remaining amount due"""
        return self.amount - self.amount_paid
    
    @property
    def is_paid(self):
        """Check if the fee is fully paid"""
        return self.amount_paid >= self.amount

class Payment(db.Model):
    """Model for payments"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    fee_id = db.Column(db.Integer, db.ForeignKey('fees.id'), nullable=False)
    
    # Payment details
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_method = db.Column(db.String(50), nullable=False)  # 'cash', 'card', 'bank_transfer', etc.
    
    # Status
    status = db.Column(db.String(20), default='pending')  # 'pending', 'completed', 'failed', 'refunded'
    
    # Transaction details
    transaction_id = db.Column(db.String(100))
    receipt_number = db.Column(db.String(100))
    
    # User info
    paid_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Student or parent
    received_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Admin or teacher
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payer = db.relationship('User', foreign_keys=[paid_by], backref='payments_made')
    receiver = db.relationship('User', foreign_keys=[received_by], backref='payments_received')
    
    def __repr__(self):
        return f'<Payment {self.id}: {self.amount}>' 
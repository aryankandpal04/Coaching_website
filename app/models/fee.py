from datetime import datetime
from app import db

class Fee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.String(20), nullable=False)  # Format: "YYYY-MM"
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue
    payment_mode = db.Column(db.String(20))  # online, cash
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    payments = db.relationship('Payment', backref='fee', lazy='dynamic')
    
    def __init__(self, amount, month, due_date, student_id):
        self.amount = amount
        self.month = month
        self.due_date = due_date
        self.student_id = student_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'month': self.month,
            'due_date': self.due_date.isoformat(),
            'status': self.status,
            'payment_mode': self.payment_mode,
            'student_id': self.student_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_mode = db.Column(db.String(20), nullable=False)  # online, cash
    transaction_id = db.Column(db.String(100))  # For online payments
    status = db.Column(db.String(20), default='pending')  # pending, success, failed
    receipt_number = db.Column(db.String(50))
    remarks = db.Column(db.Text)
    
    # Foreign Keys
    fee_id = db.Column(db.Integer, db.ForeignKey('fee.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    collected_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # Admin who collected cash
    
    def __init__(self, amount, payment_mode, fee_id, student_id):
        self.amount = amount
        self.payment_mode = payment_mode
        self.fee_id = fee_id
        self.student_id = student_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'payment_date': self.payment_date.isoformat(),
            'payment_mode': self.payment_mode,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'receipt_number': self.receipt_number,
            'remarks': self.remarks,
            'fee_id': self.fee_id,
            'student_id': self.student_id,
            'collected_by': self.collected_by
        } 
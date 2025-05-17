from datetime import datetime
from app import db

class Fee(db.Model):
    __tablename__ = 'fees'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    fee_type = db.Column(db.String(50), nullable=False)  # tuition, exam, material, etc.
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Payment tracking
    amount_paid = db.Column(db.Float, default=0.0)
    last_payment_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    
    # Optional fields
    academic_year = db.Column(db.String(20))
    semester = db.Column(db.String(20))
    discount = db.Column(db.Float, default=0.0)
    late_fee = db.Column(db.Float, default=0.0)
    
    # Relationships
    payments = db.relationship('Payment', backref='fee', lazy=True)
    
    def __init__(self, student_id, amount, fee_type, due_date, **kwargs):
        self.student_id = student_id
        self.amount = amount
        self.fee_type = fee_type
        self.due_date = due_date
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @property
    def balance(self):
        """Calculate remaining balance"""
        return self.amount + self.late_fee - self.amount_paid - self.discount
    
    def __repr__(self):
        return f'<Fee {self.id}: {self.fee_type}>'

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    fee_id = db.Column(db.Integer, db.ForeignKey('fees.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')  # pending, success, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Payment metadata
    payment_gateway = db.Column(db.String(50))
    gateway_response = db.Column(db.Text)  # Store payment gateway response
    receipt_url = db.Column(db.String(500))
    
    def __init__(self, fee_id, amount, payment_method, **kwargs):
        self.fee_id = fee_id
        self.amount = amount
        self.payment_method = payment_method
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<Payment {self.id}: {self.amount}>' 
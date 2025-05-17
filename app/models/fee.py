from datetime import datetime
from typing import Dict, Optional, List, Any
import stripe
from stripe.error import StripeError
from app import db
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

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
    def balance(self) -> float:
        """Calculate remaining balance"""
        return self.amount + self.late_fee - self.amount_paid - self.discount
    
    def check_overdue(self) -> bool:
        """Check if fee is overdue and update status"""
        try:
            if self.status != 'paid' and datetime.utcnow() > self.due_date:
                self.status = 'overdue'
                db.session.commit()
                return True
            return False
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    def apply_late_fee(self, amount: float) -> bool:
        """Apply late fee to overdue payment"""
        try:
            if self.status == 'overdue':
                self.late_fee = amount
                db.session.commit()
                return True
            return False
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    def create_payment_intent(self) -> Optional[Dict[str, Any]]:
        """Create Stripe payment intent for the fee"""
        try:
            stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
            
            # Convert amount to cents for Stripe
            amount_cents = int((self.balance) * 100)
            
            intent: stripe.PaymentIntent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='usd',
                metadata={
                    'fee_id': self.id,
                    'student_id': self.student_id,
                    'fee_type': self.fee_type
                }
            )
            
            return {
                'client_secret': intent.client_secret,
                'amount': amount_cents / 100,
                'fee_id': self.id
            }
            
        except StripeError as e:
            current_app.logger.error(f"Stripe error: {str(e)}")
            return None
        except Exception as e:
            current_app.logger.error(f"Error creating payment intent: {str(e)}")
            return None
    
    def record_payment(self, amount: float, payment_method: str, transaction_id: str) -> Optional['Payment']:
        """Record a payment for the fee"""
        try:
            payment = Payment(
                fee_id=self.id,
                amount=amount,
                payment_method=payment_method,
                transaction_id=transaction_id,
                status='success'
            )
            
            self.amount_paid += amount
            self.last_payment_date = datetime.utcnow()
            self.payment_method = payment_method
            self.transaction_id = transaction_id
            
            if self.amount_paid >= self.amount + self.late_fee - self.discount:
                self.status = 'paid'
            
            db.session.add(payment)
            db.session.commit()
            
            return payment
            
        except SQLAlchemyError:
            db.session.rollback()
            return None
    
    def get_payment_history(self) -> List[Dict]:
        """Get payment history for the fee"""
        payments = Payment.query.filter_by(fee_id=self.id).order_by(Payment.payment_date.desc()).all()
        return [{
            'id': payment.id,
            'amount': payment.amount,
            'date': payment.payment_date,
            'method': payment.payment_method,
            'status': payment.status,
            'transaction_id': payment.transaction_id,
            'receipt_url': payment.receipt_url
        } for payment in payments]
    
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
    
    def process_stripe_payment(self, payment_intent_id: str) -> bool:
        """Process a Stripe payment"""
        try:
            stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
            
            # Retrieve the payment intent
            intent: stripe.PaymentIntent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status == 'succeeded':
                self.status = 'success'
                self.gateway_response = str(intent)
                self.receipt_url = intent.charges.data[0].receipt_url if intent.charges.data else None
                
                # Update the associated fee
                fee = self.fee
                if fee:
                    fee.record_payment(
                        amount=self.amount,
                        payment_method='stripe',
                        transaction_id=payment_intent_id
                    )
                
                db.session.commit()
                return True
                
            self.status = 'failed'
            self.gateway_response = str(intent)
            db.session.commit()
            return False
            
        except StripeError as e:
            self.status = 'failed'
            self.gateway_response = str(e)
            db.session.commit()
            return False
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    def generate_receipt(self) -> Optional[Dict]:
        """Generate receipt data for the payment"""
        try:
            fee = self.fee
            if not fee:
                return None
                
            return {
                'payment_id': self.id,
                'fee_type': fee.fee_type,
                'amount': self.amount,
                'payment_date': self.payment_date,
                'payment_method': self.payment_method,
                'transaction_id': self.transaction_id,
                'status': self.status,
                'receipt_url': self.receipt_url,
                'student_id': fee.student_id,
                'academic_year': fee.academic_year,
                'semester': fee.semester
            }
            
        except Exception as e:
            current_app.logger.error(f"Error generating receipt: {str(e)}")
            return None
    
    def __repr__(self):
        return f'<Payment {self.id}: {self.amount}>' 
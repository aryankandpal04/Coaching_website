import os
import sys
import logging
from pathlib import Path
from app import create_app, db
from app.models.user import User, Role
from app.models.lecture import Course, Lecture, LectureComment, LectureView
from app.models.test import Test, Question, TestResult
from app.models.doubt import Doubt, DoubtResponse
from app.models.fee import Fee, Payment
from datetime import datetime

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure that the app directory is in the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Ensure the instance folder exists with proper permissions
instance_path = Path('D:/Coaching_website/instance')
if not instance_path.exists():
    logger.info(f"Creating instance directory at {instance_path}")
    instance_path.mkdir(parents=True, exist_ok=True)
    # On Windows, this ensures the directory is writable
    os.chmod(instance_path, 0o777)
else:
    logger.info(f"Instance directory already exists at {instance_path}")
    # Ensure proper permissions even if directory exists
    os.chmod(instance_path, 0o777)

def init_db():
    """Initialize the database with tables and sample data"""
    app = create_app()
    
    with app.app_context():
        logger.info("Creating database tables...")
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@rdlearning.com').first()
        if not admin:
            logger.info("Creating initial users...")
            # Create admin user
            admin = User(
                email='admin@rdlearning.com',
                username='admin',
                role='admin',
                first_name='Admin',
                last_name='User',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create test teacher account
            teacher = User(
                email='teacher@rdlearning.com',
                username='teacher',
                role='teacher',
                first_name='Test',
                last_name='Teacher',
                subjects='Mathematics,Physics',
                qualifications='M.Sc, B.Ed',
                is_active=True
            )
            teacher.set_password('teacher123')
            db.session.add(teacher)
            
            # Create test student account
            student = User(
                email='student@rdlearning.com',
                username='student',
                role='student',
                first_name='Test',
                last_name='Student',
                grade=10,
                is_active=True
            )
            student.set_password('student123')
            db.session.add(student)
            
            # Create test parent account
            parent = User(
                email='parent@rdlearning.com',
                username='parent',
                role='parent',
                first_name='Test',
                last_name='Parent',
                is_active=True
            )
            parent.set_password('parent123')
            db.session.add(parent)
            
            try:
                db.session.commit()
                logger.info("Database initialized successfully!")
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error initializing database: {str(e)}")
                raise
        else:
            logger.info("Database already initialized.")

if __name__ == '__main__':
    init_db()
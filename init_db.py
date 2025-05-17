import os
import sys
import logging
from pathlib import Path
from app import create_app, db
from app.models.user import User
from app.models.lecture import Lecture, LectureComment, LectureView
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
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@rdlearning.com').first()
        if not admin:
            # Create admin user
            admin = User(
                email='admin@rdlearning.com',
                username='admin',
                role='admin',
                first_name='Admin',
                last_name='User',
                is_active=True
            )
            admin.set_password('admin123')  # Set a secure password in production
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
            
            # Link student to parent
            student.parent_id = parent.id
            
            # Create sample lecture
            lecture = Lecture(
                title='Introduction to Algebra',
                description='Basic concepts of algebra and its applications',
                subject='Mathematics',
                grade=10,
                author_id=teacher.id,
                content='Learn about variables, expressions, and equations...',
                video_url='https://example.com/intro-algebra.mp4',
                duration=45,
                difficulty_level='beginner',
                is_published=True
            )
            db.session.add(lecture)
            
            # Create sample test
            test = Test(
                title='Algebra Basics Test',
                description='Test your understanding of basic algebra concepts',
                subject='Mathematics',
                grade=10,
                creator_id=teacher.id,
                duration=60,
                total_marks=50,
                passing_marks=25,
                is_published=True
            )
            db.session.add(test)
            
            # Create sample questions
            question1 = Question(
                test_id=1,
                question_text='What is the value of x in 2x + 5 = 15?',
                question_type='mcq',
                marks=5,
                correct_answer='5'
            )
            question1.set_options(['3', '4', '5', '6'])
            db.session.add(question1)
            
            # Create sample doubt
            doubt = Doubt(
                title='Help with Quadratic Equations',
                description='I am having trouble solving quadratic equations...',
                subject='Mathematics',
                grade=10,
                student_id=student.id,
                priority='normal'
            )
            db.session.add(doubt)
            
            # Create sample fee
            fee = Fee(
                student_id=student.id,
                amount=5000.0,
                fee_type='tuition',
                due_date=datetime(2024, 5, 1),
                academic_year='2024-25',
                semester='Spring'
            )
            db.session.add(fee)
            
            db.session.commit()
            print('Database initialized with sample data!')

if __name__ == '__main__':
    init_db()
from app import create_app, db
from app.models.user import User
from app.models.lecture import Lecture, LectureComment, LectureView
from app.models.test import Test, Question, TestResult
from app.models.doubt import Doubt, DoubtResponse
from app.models.fee import Fee, Payment
from flask_migrate import upgrade
import click
import os

# Create the application instance
app = create_app()

# Create a context for database operations
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Lecture': Lecture,
        'LectureComment': LectureComment,
        'LectureView': LectureView,
        'Test': Test,
        'Question': Question,
        'TestResult': TestResult,
        'Doubt': Doubt,
        'DoubtResponse': DoubtResponse,
        'Fee': Fee,
        'Payment': Payment
    }

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # Migrate database to latest revision
    upgrade()

@app.cli.command()
@click.argument('email')
@click.argument('password')
def create_admin(email, password):
    """Create a new admin user."""
    user = User.query.filter_by(email=email).first()
    if user:
        click.echo('User already exists!')
        return
    
    user = User(
        email=email,
        username=email.split('@')[0],
        role='admin',
        first_name='Admin',
        last_name='User',
        is_active=True
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo('Admin user created successfully!')

@app.cli.command()
def init_db():
    """Initialize the database."""
    click.echo('Creating database tables...')
    db.create_all()
    click.echo('Database tables created!')

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 
import os
import sys
import logging
from pathlib import Path

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

# Create application context
from app import create_app, db
from app.models.user import User, Role

app = create_app()

with app.app_context():
    logger.info("Creating database tables...")
    db.create_all()
    logger.info("Database tables created!")

    # Rest of your initialization code...
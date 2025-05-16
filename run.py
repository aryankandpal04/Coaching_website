import os
from app import create_app, db
from flask_migrate import upgrade

# Create the application instance
app = create_app(os.getenv("FLASK_ENV", "development"))

# Create a context for database operations
@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        # Import models here to make them available in the shell
        # Example: "User": User
    }

# Command to create an admin user
@app.cli.command("create-admin")
def create_admin():
    """Create an admin user"""
    from app.models.user import User, Role
    
    # Check if admin role exists
    admin_role = Role.query.filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin", description="Administrator")
        db.session.add(admin_role)
    
    # Check if admin user exists
    admin = User.query.filter_by(email="admin@rdlearningplanet.com").first()
    if admin:
        print("Admin already exists.")
        return
    
    # Create admin user
    admin = User(
        email="admin@rdlearningplanet.com",
        username="admin",
        first_name="Admin",
        last_name="User",
    )
    admin.set_password("admin123")  # Change in production!
    admin.roles.append(admin_role)
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully.")

if __name__ == "__main__":
    app.run() 
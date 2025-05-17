# RD Learning Planet

A comprehensive web platform for students (Class 6-12), teachers, parents, and admin team to manage online learning.

## Features

- **User Management**
  - Role-based access control (Admin, Teacher, Student, Parent)
  - Secure authentication and authorization
  - Profile management

- **Learning Management**
  - Video lectures with interactive features
  - Course materials and resources
  - Progress tracking
  - Bookmarking and notes

- **Mock Test System**
  - Multiple choice and subjective tests
  - Automated grading
  - Performance analytics
  - Test scheduling

- **Doubt Resolution**
  - Real-time doubt posting
  - Teacher responses
  - Doubt tracking
  - File attachments

- **Fee Management**
  - Online fee payment
  - Payment history
  - Receipt generation
  - Due date reminders

- **Performance Analytics**
  - AI-powered learning insights
  - Progress reports
  - Performance comparisons
  - Improvement suggestions

## Tech Stack

- **Frontend**
  - HTML5, CSS3
  - Bootstrap 5
  - JavaScript
  - Chart.js for visualizations
  - AOS.js for animations

- **Backend**
  - Python 3.8+
  - Flask framework
  - SQLAlchemy ORM
  - Flask extensions

- **Database**
  - SQLite (Development)
  - PostgreSQL (Production)

- **Additional Tools**
  - Redis for caching
  - Celery for background tasks
  - Firebase for notifications
  - Stripe for payments

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/rd-learning-planet.git
   cd rd-learning-planet
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   flask init-db
   ```

6. Create an admin user:
   ```bash
   flask create-admin admin@rdlearning.com password123
   ```

7. Run the development server:
   ```bash
   flask run
   ```

The application will be available at `http://localhost:5000`

## Development

1. Run tests:
   ```bash
   flask test
   ```

2. Database migrations:
   ```bash
   flask db migrate -m "Migration message"
   flask db upgrade
   ```

3. Shell context:
   ```bash
   flask shell
   ```

## Deployment

1. Set up production environment variables
2. Configure PostgreSQL database
3. Set up Redis server
4. Configure email server
5. Set up Stripe for payments
6. Configure Firebase for notifications
7. Run database migrations
8. Start the application with gunicorn

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@rdlearning.com or create an issue in the repository. 
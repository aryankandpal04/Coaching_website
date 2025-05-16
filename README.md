# RD Learning Planet

A comprehensive web application for classes 6 to 12 that streamlines student learning, mock test management, fees tracking, doubt solving, and performance evaluation, with role-based access for Admins, Teachers, Students, and Parents.

## 🚀 Features

- **User Management**: Role-based access control for Admins, Teachers, Students, and Parents
- **Learning Management**: Upload and access lectures and learning materials
- **Mock Test System**: Create, manage, and take tests with automatic grading
- **Performance Tracking**: Detailed analytics and reports for students
- **Doubt Solving**: Interactive platform for students to ask questions and get answers
- **Fee Management**: Track and manage student fees and payments

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3
- Bootstrap 5
- JavaScript (Vanilla)
- AOS.js (Animations)
- Chart.js (Performance visualization)
- Swiper.js (Carousels)
- SweetAlert2 (Enhanced alerts)

### Backend
- Python 3.9+
- Flask Framework
- SQLAlchemy ORM
- Flask-Login (Authentication)
- Flask-WTF (Forms)
- Flask-Mail (Email notifications)
- Pandas (Data analysis)

### Database
- SQLite (Development)
- PostgreSQL (Production)

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rd-learning-planet.git
   cd rd-learning-planet
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (create a `.env` file):
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Create an admin user:
   ```bash
   flask create-admin
   ```

7. Run the application:
   ```bash
   flask run
   ```

8. Access the application at `http://localhost:5000`

## 👥 User Roles

- **Admin**: Full access to all features, user management, and system settings
- **Teacher**: Upload lectures, create and manage tests, answer doubts, view student performance
- **Student**: Access lectures, take tests, ask doubts, view personal performance
- **Parent**: View child's performance, pay fees, communicate with teachers

## 📊 Database Schema

The application uses the following main models:
- User (with role-based permissions)
- Course
- Lecture
- MockTest
- Question
- TestAttempt
- Doubt
- Payment

## 🧪 Testing

Run tests using pytest:
```bash
pytest
```

Generate coverage report:
```bash
coverage run -m pytest
coverage report
```

## 🚀 Deployment

### Development
```bash
flask run
```

### Production (with Gunicorn)
```bash
gunicorn "app:create_app('production')"
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For any inquiries, please contact [your-email@example.com](mailto:your-email@example.com) 
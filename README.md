# RD Learning Planet

A comprehensive, interactive, and intelligent coaching web application for students from Class 6 to Class 12, their teachers, parents, and admin team.

## Features

### Core Features
- Multi-role authentication (Admin, Teacher, Student, Parent)
- Video lecture management
- Mock test system with MCQ and written formats
- Doubt resolution system
- Fee management
- Performance tracking and analytics

### Advanced Features
- AI-powered learning insights
- Interactive video lectures with bookmarks
- Gamified learning experience
- Real-time notifications
- Smart resource center
- Mobile-optimized interface (PWA)

## Tech Stack

### Frontend
- HTML5, CSS3, Bootstrap 5
- JavaScript (Vanilla)
- Chart.js for visualizations
- AOS.js for animations
- SweetAlert2 for alerts
- Video.js for video playback

### Backend
- Python 3.8+
- Flask framework
- SQLAlchemy ORM
- Flask-Login for authentication
- Celery for background tasks
- Redis for caching

### Database
- SQLite (Development)
- PostgreSQL (Production)

### AI/ML Components
- scikit-learn for analytics
- TensorFlow for advanced features
- OpenAI API for chatbot

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rd-learning-planet.git
cd rd-learning-planet
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the development server:
```bash
flask run
```

## Project Structure

```
rd-learning-planet/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   │   ├── admin/
│   │   ├── teacher/
│   │   ├── student/
│   │   └── parent/
│   ├── models/
│   └── utils/
├── migrations/
├── tests/
├── venv/
├── config.py
├── requirements.txt
└── run.py
```

## User Roles

### Admin
- Full system access
- User management
- Content management
- Fee management
- Analytics access

### Teacher
- Upload lectures
- Create/evaluate tests
- Respond to doubts
- Track student performance

### Student
- Watch lectures
- Take tests
- Ask doubts
- View progress

### Parent
- View child's performance
- Pay fees
- Communicate with teachers

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - your.email@example.com
Project Link: https://github.com/yourusername/rd-learning-planet 
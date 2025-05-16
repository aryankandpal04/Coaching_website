# Import models here for easy access
from app.models.user import User, Role
from app.models.mock_test import MockTest, Question, TestAttempt, Answer
from app.models.lecture import Course, Lecture, LectureAttachment, LectureView
from app.models.doubt import Doubt, DoubtResponse, DoubtAttachment, DoubtResponseAttachment
from app.models.payment import Fee, Payment
from app.models.notification import Notification, Announcement 
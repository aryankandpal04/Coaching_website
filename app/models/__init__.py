# Import models here for easy access
from app.models.user import User, Role
from app.models.lecture import Course, Lecture, LectureComment, LectureView
from app.models.test import Test, Question, TestResult, Result, Answer
from app.models.doubt import Doubt, DoubtResponse, DoubtAttachment, DoubtResponseAttachment
from app.models.fee import Fee, Payment

__all__ = [
    'User', 'Role',
    'Course', 'Lecture', 'LectureComment', 'LectureView',
    'Test', 'Question', 'TestResult', 'Result', 'Answer',
    'Doubt', 'DoubtResponse', 'DoubtAttachment', 'DoubtResponseAttachment',
    'Fee', 'Payment'
] 
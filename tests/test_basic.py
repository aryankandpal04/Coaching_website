import unittest
from flask import current_app
from app import create_app, db

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_app_exists(self):
        self.assertIsNotNone(current_app)
        
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
        
if __name__ == '__main__':
    unittest.main() 
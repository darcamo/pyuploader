import unittest
import sys
sys.path.append('../')

from app import db, app



class CommonTester(unittest.TestCase):
    def common_setup_code(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        # Use a memory sqlite database for testing, since it is much faster
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.app = app.test_client()
        db.create_all()

    def common_teardown_code(self):
        # Notice also that db.session.remove() is called at the end of each
        # test, to ensure the SQLAlchemy session is properly removed and that
        #  a new session is started with each test run - this is a common
        # “gotcha”.
        db.session.remove()
        db.drop_all()

    def setUp(self):
        # If you reimplement setUp in a subclass call the common_setup_code
        # method in the beggining of your setUp method
        self.common_setup_code()

    def tearDown(self):
        # If you reimplement tearDown in a subclass call the
        # common_teardown_code method in the beggining of your tearDown method
        self.common_teardown_code()

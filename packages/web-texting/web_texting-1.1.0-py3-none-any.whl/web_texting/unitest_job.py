
import unittest
from .web_job import WebJobHandler


def test_func():
    pass


class JobTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("execute setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("execute tearDownClass")

    def setUp(self):
        print("execute setUp")

    def tearDown(self):
        print("execute tearDown")

    def set_job(self, data):
        self.step_handler = WebJobHandler(data)
        job_id = self.step_handler._job_id
        test_method = 'test_' + job_id
        setattr(self, test_method, test_func)
        return test_method

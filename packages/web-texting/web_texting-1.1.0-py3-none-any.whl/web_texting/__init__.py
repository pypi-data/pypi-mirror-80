import traceback
import unittest
from .web_job import WebJobHandler
from .unitest_job import JobTest

__all__ = [
    "run"
]

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run(data, on_job, on_step, gen_html_rpt=False):
    step_handler = WebJobHandler(data)
    try:
        step_handler.run(on_job, on_step)
    except Exception as exp:
        logger.exception(exp)
    if gen_html_rpt:
        step_handler.gen_html_rpt()


def run_suite(data):
    try:
        suite = unittest.TestSuite()
        suite.addTest()
    except Exception as exp:
        # traceback.extract_stack(exp)
        logger.exception(exp)
    pass

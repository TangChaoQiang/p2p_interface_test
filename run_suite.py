import requests
import unittest
import time
from app import base_dir
from scripts.login import login
from scripts.approve import approve
from scripts.trust import trust_test
from lib.HTMLTestRunner_PY3 import HTMLTestRunner
from scripts.work_flow import work_flow

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(login))
suite.addTest(unittest.makeSuite(approve))
suite.addTest(unittest.makeSuite(trust_test))
suite.addTest(unittest.makeSuite(work_flow))


# report_file = base_dir + "/report/report{}.html".format(time.strftime("%Y%m%d-%H%M%S"))
report_file = base_dir + "/report/report.html"

with open(report_file, "wb") as f:
    runner = HTMLTestRunner(f, title="p2p_金融项目", description="test")
    runner.run(suite)

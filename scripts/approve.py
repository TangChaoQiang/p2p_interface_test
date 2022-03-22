import logging
import unittest
import requests
import utils
from api.approveAPI import approveAPI
from api.loginAPI import loginAPI


class approve(unittest.TestCase):
    phone1 = "15666666661"
    phone2 = "15666666662"
    phone5 = "15666666665"
    card_id = "220202198908194409"
    def setUp(self):
        self.session = requests.session()
        self.approve = approveAPI()
        self.login = loginAPI()
    def tearDown(self):
        self.session.close()

    def test01_approve_success(self):
        response = self.login.login(self.session, keywords=self.phone1)
        response = self.approve.Approve(session=self.session, card_id=self.card_id)
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "提交成功!")

    def test02_approve_fail_NO_name(self):
        response = self.login.login(self.session, keywords=self.phone2)
        print(response.json())
        response = self.approve.Approve(session=self.session, realname='', card_id=self.card_id)
        print(response.json())
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "姓名不能为空")

    def test03_approve_fail_NO_id(self):
        response = self.login.login(self.session, keywords=self.phone2)
        print(response.json())
        response = self.approve.Approve(session=self.session, card_id='')
        print(response.json())
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "身份证号不能为空")

    def test04_approve_fail_Occur_id(self):
        response = self.login.login(self.session, keywords=self.phone2)
        print(response.json())
        response = self.approve.Approve(session=self.session, card_id=self.card_id)
        print(response.json())
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "身份证号已存在")

    def test05_isapprove(self):
        response = self.login.login(self.session, keywords=self.phone1)
        response = self.approve.isApprove(self.session)
        logging.info("get message = {}".format(response.json()))
        self.assertEqual(200, response.status_code)

    def test06_isapprove(self):
        # response = self.login.login(self.session, keywords=self.phone1)
        response = self.approve.isApprove(self.session)
        # print(response.json())
        self.assertEqual(200, response.status_code)
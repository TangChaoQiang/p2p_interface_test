import logging
import random
import unittest

import requests

import utils
from api.loginAPI import loginAPI
from api.trustAPI import trustAPI
from api.tenderAPI import tenderAPI

class tender_test(unittest.TestCase):
    phone2 = "15666666662"
    def setUp(self):
        self.session = requests.session()
        self.login = loginAPI()
        self.trust = trustAPI()
        self.tender = tenderAPI()

    def tearDown(self):
        self.session.close()

    def test01_tender_success(self):
        # 获取登录
        response = self.login.login(self.session, self.phone2)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
        # 获取验证码
        r = random.randint(10000, 99999)
        response = self.trust.get_verifycode(self.session, str(r))
        # logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        # 充值
        response = self.trust.recharge(self.session)
        logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        #获取form值
        form_data = response.json().get("description").get("form")
        logging.info("get response = {}".format(form_data))
        #风险测评
        response = self.tender.risk_appraisal(self.session)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "OK")
        #第三方接口调用
        response = utils.third_requests(self, form_data)
        logging.info("get response = {}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)

        response = self.tender.tender(self.session)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "该标已被投满")

    def test02_passwd_not(self):
        # 获取登录
        response = self.login.login(self.session, self.phone2)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
        # 获取验证码
        r = random.randint(10000, 99999)
        response = self.trust.get_verifycode(self.session, str(r))
        # logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        # 充值
        response = self.trust.recharge(self.session)
        logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)

        response = self.tender.tender(self.session, depositCertificate="")
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "投资密码不能为空")

    def test03_passwd_not(self):
        # 获取登录
        response = self.login.login(self.session, self.phone2)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
        # 获取验证码
        r = random.randint(10000, 99999)
        response = self.trust.get_verifycode(self.session, str(r))
        # logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        # 充值
        response = self.trust.recharge(self.session)
        logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)

        response = self.tender.tender(self.session,amount="")
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "不是正确的金额")

    def test04_mytenderlist(self):
        # 获取登录
        response = self.login.login(self.session, self.phone2)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
        # 获取验证码
        r = random.randint(10000, 99999)
        response = self.trust.get_verifycode(self.session, str(r))
        # logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        # 充值
        response = self.trust.recharge(self.session)
        logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        # 获取form值
        form_data = response.json().get("description").get("form")
        logging.info("get response = {}".format(form_data))
        # 风险测评
        response = self.tender.risk_appraisal(self.session)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "OK")
        # 第三方接口调用
        response = utils.third_requests(self, form_data)
        logging.info("get response = {}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)
        #三方投资
        response = self.tender.tender(self.session)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "该标已被投满")

        #查看投资列表

        response = self.tender.mytenderlist(self.session, "tender")
        logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)

        response = self.tender.mytenderlist(self.session, "recover")
        logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)

        response = self.tender.mytenderlist(self.session, "recover_yes")
        logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)

        response = self.tender.mytenderlist(self.session, "over")
        logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)


import unittest
import requests
from api.tenderAPI import tenderAPI
from api.trustAPI import trustAPI
from api.loginAPI import loginAPI
from api.approveAPI import approveAPI
import random
import utils
import logging
import app

class work_flow(unittest.TestCase):
    phone7 = "15666666662"
    Img_Code = "8888"
    card_id = "220202198908194409"

    @classmethod
    def setUpClass(cls):
        cls.session = requests.session()
        cls.login = loginAPI()
        cls.approve = approveAPI()
        cls.trust = trustAPI()
        cls.tender = tenderAPI()

    @classmethod
    def tearDownClass(cls):
        print("-------------------------------------------------------------------")
        cls.session.close()
        sql1 = "DELETE i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id where m.phone like '15666666%'"
        utils.DB_mysql.delete(app.DB_member, sql1)
        logging.info("get response = {}".format(sql1))
        sql2 = "DELETE l.* from mb_member_login_log l INNER JOIN mb_member m on l.member_id = m.id where m.phone  like '15666666%'"
        utils.DB_mysql.delete(app.DB_member, sql2)
        logging.info("get response = {}".format(sql2))
        sql3 = "delete from mb_member where phone like '15666666%'"
        utils.DB_mysql.delete(app.DB_member, sql3)
        logging.info("get response = {}".format(sql3))
        sql4 = "DELETE from mb_member_register_log where phone like  '15666666%'"
        utils.DB_mysql.delete(app.DB_member, sql4)
        logging.info("get response = {}".format(sql4))

    def test01_work_flow(self):
        #1.获取图片验证码
        r = random.randint(0, 1000)
        response = self.login.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)

        # 2.获取短信验证码
        response = self.login.getPhoneCode(self.session, self.phone7, self.Img_Code)
        print(response.json())
        utils.assert_utils(self, response, 200, 200, "短信发送成功")
        logging.info("get message = {}".format(response.json()))

        # 3.注册
        response = self.login.register(self.session, self.phone7)
        print(response.json())
        utils.assert_utils(self, response, 200, 200, "注册成功")
        logging.info("get message = {}".format(response.json()))

        #4.登录成功
        response = self.login.login(self.session, self.phone7)
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")

        #5.开户成功
        # 获取登录
        # 开户成功
        response = self.trust.register(self.session)
        logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))

        # 获取返回值中form的数据
        form_data = response.json().get("description").get("form")
        logging.info("get response = {}".format(form_data))

        #6.请求三方开户成功
        response = utils.third_requests(self, form_data)
        logging.info("get response = {}".format(response))
        self.assertEqual(200, response.status_code)

        #7.获取充值图片验证码、第三方充值成功
        # 获取登录
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
        response = utils.third_requests(self, form_data)
        self.assertEqual(200, response.status_code)

        #8.投资成功
        # 风险测评
        response = self.tender.risk_appraisal(self.session)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "OK")
        # 第三方接口调用
        response = utils.third_requests(self, form_data)
        logging.info("get response = {}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)

        response = self.tender.tender(self.session)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "该标已被投满")



import logging
import random
import utils
import requests
import unittest
from api.trustAPI import trustAPI
from api.loginAPI import loginAPI
from bs4 import BeautifulSoup

class trust_test(unittest.TestCase):
    phone2 = "15666666662"
    def setUp(self):
        self.session = requests.session()
        self.trust = trustAPI()
        self.login = loginAPI()

    def tearDown(self):
        self.session.close()

    def test01_register_success(self):
        #获取登录
        response = self.login.login(self.session, self.phone2)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
        #开户成功
        response = self.trust.register(self.session)
        logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        #获取返回值中form的数据
        form_data = response.json().get("description").get("form")
        logging.info("get response = {}".format(form_data))
        # #定义Beautiful对象
        # soup = BeautifulSoup(form_data, "html.parser")
        # #获取第三方接口的URL地址
        # third_url = soup.form['action']
        # logging.info("get response = {}".format(third_url))
        # #定义字典获取参数值
        # data = {}
        # for i in soup.find_all('input'):
        #     data.setdefault(i["name"], i["value"])
        # #发送请求
        # response = requests.post(third_url, data=data)
        # logging.info("get response = {}".format(third_url))
        # self.assertEqual(200, response.status_code)
        response = utils.third_requests(self, form_data)
        logging.info("get response = {}".format(response))
        self.assertEqual(200, response.status_code)

    def test02_getcode_success_float_success(self):
        # 获取登录
        response = self.login.login(self.session, self.phone2)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
        #获取验证码
        r = random.randint(10000, 99999)
        response = self.trust.get_verifycode(self.session, str(r))
        # logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)

    def test03_getcode_success_int_success(self):
        # 获取登录
        response = self.login.login(self.session, self.phone2)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
        #获取随机数
        r = random.random()
        response = self.trust.get_verifycode(self.session, str(r))
        # logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)

    def test04_notcode_fail(self):
        # 获取登录
        response = self.login.login(self.session, self.phone2)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
        r=''
        response = self.trust.get_verifycode(self.session, str(r))
        # logging.info("get response = {}".format(response.json()))
        self.assertEqual(404, response.status_code)

    def test05_charcode_fail(self):
        # 获取登录
        response = self.login.login(self.session, self.phone2)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
        # 获取随机数
        r = random.sample("abcdeghijklm", 3)
        r=''.join(r)
        # print(r)
        response = self.trust.get_verifycode(self.session, str(r))
        # logging.info("get response = {}".format(response.json()))
        self.assertEqual(400, response.status_code)

    def test06_recharge_success(self):
        # 获取登录
        response = self.login.login(self.session, self.phone2)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
        # 获取验证码
        r = random.randint(10000, 99999)
        response = self.trust.get_verifycode(self.session, str(r))
        # logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        #充值
        response = self.trust.recharge(self.session)
        logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        #获取form值
        form_data = response.json().get("description").get("form")
        logging.info("get response = {}".format(form_data))
        response = utils.third_requests(self, form_data)
        self.assertEqual(200, response.status_code)


    def test07_noMoneny_recharge_fail(self):
        # 获取登录
        response = self.login.login(self.session, self.phone2)
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
        # 获取验证码
        r = random.randint(10000, 99999)
        response = self.trust.get_verifycode(self.session, str(r))
        # logging.info("get response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        #充值
        response = self.trust.recharge(self.session, amount=" ")
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "充值金额不能为空")

    def test08_failcode_recharge_fail(self):
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
        response = self.trust.recharge(self.session, valicode="2222")
        logging.info("get response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "验证码错误")

import logging
from time import sleep

from api.loginAPI import loginAPI
import unittest
import requests
import random
import utils

class login(unittest.TestCase):
    phone1 = "15666666661"
    phone2 = "15666666662"
    phone3 = "15666666663"
    phone4 = "15666666664"
    phone5 = "15666666665"
    phone6 = "15666666666"
    Img_Code = "8888"
    Phone_code = "666666"

    def setUp(self):
        self.login_api = loginAPI()
        self.session = requests.Session()

    def tearDown(self):
        self.session.close()

    def test001_getImgcode_random(self):              #获取随机小数（成功）
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)

    def test002_getImgcode_random(self):              #获取随机整数（成功）
        r = random.randint(0,1000)
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)

    def test003_getImgcode_random(self):              #获取随机数为空（失败）
        r = ""
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 400 | 404)

    def test004_getImgcode_random(self):              #获取随机字符串（失败）
        r = random.sample("abcdefghijk", 3)
        ran = ''.join(r)
        response = self.login_api.getImgCode(self.session, str(ran))
        self.assertEqual(response.status_code, 400)


    def test005_getPhoneCode(self):                   #获取短信验证码成功（参数正确）
        #1.获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)

        #2.获取短信验证码
        response = self.login_api.getPhoneCode(self.session, self.phone1,self.Img_Code)
        print(response.json())
        utils.assert_utils(self, response, 200, 200, "短信发送成功")
        logging.info("get message = {}".format(response.json()))

        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json().get("status"), 200)
        # self.assertEqual(response.json().get("description"), "短信发送成功")

    def test006_getPhoneCode(self):                     # 获取短信验证码失败（图片验证码错误）
        # 1.获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)

        # 2.获取短信验证码
        response = self.login_api.getPhoneCode(self.session, self.phone1, 8886)
        utils.assert_utils(self, response, 200, 100, "图片验证码错误")
        logging.info("get message = {}".format(response.json()))
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json().get("status"), 100)
        # self.assertEqual(response.json().get("description"), "图片验证码错误")

    def test007_getPhoneCode(self):                     # 获取短信验证码失败（手机号为空）
        # 1.获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)

        # 2.获取短信验证码
        response = self.login_api.getPhoneCode(self.session, '', self.Img_Code)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 100)
        logging.info("get message = {}".format(response.json()))


    def test008_getPhoneCode(self):                     # 获取短信验证码失败（图片验证码为空）
        # 1.获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)

        # 2.获取短信验证码
        response = self.login_api.getPhoneCode(self.session, self.phone1, '')
        utils.assert_utils(self, response, 200, 100, "图片验证码错误")
        logging.info("get message = {}".format(response.json()))
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json().get("status"), 100)
        # self.assertEqual(response.json().get("description"), "图片验证码错误")

    def test009_getPhoneCode(self):                     # 获取短信验证码失败（未调用图片验证码接口）

        # 获取短信验证码
        response = self.login_api.getPhoneCode(self.session, self.phone1, self.Img_Code)
        utils.assert_utils(self, response, 200, 100, "图片验证码错误")
        logging.info("get message = {}".format(response.json()))


    def test010_register(self):                                                #注册成功（必填参数正确）
        # 1.获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)

        # 2.获取短信验证码
        response = self.login_api.getPhoneCode(self.session, self.phone1, self.Img_Code)
        utils.assert_utils(self, response, 200, 200, "短信发送成功")
        #3.注册
        response = self.login_api.register(self.session, self.phone1)
        print(response.json())
        utils.assert_utils(self, response, 200, 200, "注册成功")
        logging.info("get message = {}".format(response.json()))

    def test011_register(self):                                               #注册成功（所有参数正确）
        # 1.获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)
        # 2.获取短信验证码
        response = self.login_api.getPhoneCode(self.session, self.phone2, self.Img_Code)
        utils.assert_utils(self, response, 200, 200, "短信发送成功")
        #3.注册
        response = self.login_api.register(self.session, self.phone2, invite_phone= "15666666661")
        print(response.json())
        utils.assert_utils(self, response, 200, 200, "注册成功")
        logging.info("get message = {}".format(response.json()))

    def test012_register(self):                                               #注册失败（图片验证码错误）
        # 1.获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)
        # 2.获取短信验证码
        response = self.login_api.getPhoneCode(self.session, self.phone3, self.Img_Code)
        utils.assert_utils(self, response, 200, 200, "短信发送成功")
        #3.注册
        response = self.login_api.register(self.session, self.phone3, Img_code='8889')
        print(response.json())
        utils.assert_utils(self, response, 200, 100, "验证码错误!")
        logging.info("get message = {}".format(response.json()))

    def test013_register(self):                                               #注册失败（短信验证码错误）
        # 1.获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)
        # 2.获取短信验证码
        response = self.login_api.getPhoneCode(self.session, self.phone4, self.Img_Code)
        utils.assert_utils(self, response, 200, 200, "短信发送成功")
        #3.注册
        response = self.login_api.register(self.session, self.phone4, phone_code='666665')
        print(response.json())
        utils.assert_utils(self, response, 200, 100, "验证码错误")
        logging.info("get message = {}".format(response.json()))

    def test014_register(self):                                               #注册失败（手机已经存在）
        # 1.获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)
        # 2.获取短信验证码
        response = self.login_api.getPhoneCode(self.session, self.phone1, self.Img_Code)
        utils.assert_utils(self, response, 200, 200, "短信发送成功")
        #3.注册
        response = self.login_api.register(self.session, self.phone1, phone_code='666665')
        print(response.json())
        utils.assert_utils(self, response, 200, 100, "手机已存在!")
        logging.info("get message = {}".format(response.json()))

    def test015_register(self):                                               #注册失败（密码为空）
        # 1.获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)
        # 2.获取短信验证码
        response = self.login_api.getPhoneCode(self.session, self.phone5, self.Img_Code)
        utils.assert_utils(self, response, 200, 200, "短信发送成功")
        #3.注册
        response = self.login_api.register(self.session, self.phone5, pwd='')
        print(response.json())
        utils.assert_utils(self, response, 200, 100, "密码不能为空")
        logging.info("get message = {}".format(response.json()))

    def test016_register(self):                                               #注册失败（未同意协议）
        # 1.获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(response.status_code, 200)
        # 2.获取短信验证码
        response = self.login_api.getPhoneCode(self.session, self.phone6, self.Img_Code)
        utils.assert_utils(self, response, 200, 200, "短信发送成功")
        #3.注册
        response = self.login_api.register(self.session, self.phone6, server="0ff")
        print(response.json())
        utils.assert_utils(self, response, 200, 100, "请同意我们的条款")
        logging.info("get message = {}".format(response.json()))

    def test017_login_success(self):
        response = self.login_api.login(self.session, self.phone1)
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")

    def test018_login_fail(self):                                  #登录失败（用户不存在）
        response = self.login_api.login(self.session, keywords="15213364334")
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "用户不存在")

    def test019_login_fail(self):                                  #登录失败（密码为空）
        response = self.login_api.login(self.session, self.phone1, password='')
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "密码不能为空")

    # def test020_login_fail(self):                                  #登录失败（密码错误一次）
    #     response = self.login_api.login(self.session, self.phone1, password='t1234567')
    #     logging.info("get message = {}".format(response.json()))
    #     utils.assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")
    #
    # def test021_login_fail(self):                                  #登录失败（密码错误两次）
    #     response = self.login_api.login(self.session, self.phone1, password='t1234568')
    #     response = self.login_api.login(self.session, self.phone1, password='t1234568')
    #     logging.info("get message = {}".format(response.json()))
    #     utils.assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")

    def test020_login_fail(self):  # 登录失败（密码错误三次）
        response = self.login_api.login(self.session, self.phone1, password='t1234568')
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")
        response = self.login_api.login(self.session, self.phone1, password='t1234568')
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")
        response = self.login_api.login(self.session, self.phone1, password='t1234568')
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

    def test021_login_success(self):
        sleep(60)
        response = self.login_api.login(self.session, self.phone1)
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")

    def test022_islogin_success(self):
        response = self.login_api.login(self.session, self.phone1)
        utils.assert_utils(self, response, 200, 200, "登录成功")


        response = self.login_api.islogin(self.session)
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "OK")

    def test023_islogin_fail(self):
        response = self.login_api.islogin(self.session)
        logging.info("get message = {}".format(response.json()))
        utils.assert_utils(self, response, 200,250, "您未登陆！")













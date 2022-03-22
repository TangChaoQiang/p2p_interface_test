import app


class loginAPI():
    def __init__(self):
        self.ContentType = "application/x-www-form-urlencoded"
        self.getImgCode_url = app.Base_url + "/common/public/verifycode1/"
        self.getPhoneCode_url = app.Base_url + "/member/public/sendSms"
        self.register_url = app.Base_url + "/member/public/reg"
        self.login_url = app.Base_url + "/member/public/login"
        self.islogin_url = app.Base_url + "/member/public/islogin"

    def getImgCode(self, session, r):
        url = self.getImgCode_url + r
        return session.get(url)

    def getPhoneCode(self, session, phone1, imgcode):
        data1 = {"phone": phone1, "imgVerifyCode": imgcode, "type":"reg"}
        return session.post(url=self.getPhoneCode_url, data=data1)

    def register(self,session, phone1, pwd='t123456', Img_code='8888', phone_code='666666', server='on', invite_phone=''):
        data = {"phone":phone1, "password":pwd, "verifycode":Img_code, "phone_code":phone_code, "dy_server":server, "invite_phone":invite_phone}
        return session.post(url=self.register_url, data=data)

    def login(self, session, keywords, password="t123456"):
        data = {"keywords":keywords, "password": password}
        return session.post(url=self.login_url, data=data)

    def islogin(self, session):
        return session.post(self.islogin_url)
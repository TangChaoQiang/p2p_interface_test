import app


class trustAPI():
    def __init__(self):
        self.register_url = app.Base_url + "/trust/trust/register"
        self.get_verifycode_url = app.Base_url + "/common/public/verifycode/"
        self.recharge_url = app.Base_url + "/trust/trust/recharge"

    def register(self, session):
        url = self.register_url
        return session.post(url)

    def get_verifycode(self, session, r):
        url = self.get_verifycode_url + r
        return session.post(url)

    def recharge(self, session, paymentType="chinapnrTrust", amount="10000", formStr="reFrom", valicode="8888"):
        url = self.register_url
        data = {
            "paymentType": paymentType,
            "amount":amount,
            "formStr":formStr,
            "valicode":valicode
        }
        return session.post(url=url, data=data)

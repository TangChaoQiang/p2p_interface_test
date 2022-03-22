from app import Base_url
import unittest

class approveAPI():
    def __init__(self):
        self.ContentType = "application/x-www-form-urlencoded"
        self.Approve_url = Base_url + "/member/realname/approverealname"
        self.isApprove_url = Base_url + "/member/member/getapprove"

    def Approve(self,session, realname="张三", card_id=''):
        data = {
            "realname": realname,
            "card_id": card_id
        }
        return session.post(url=self.Approve_url, data=data, files={'x': 'y'})

    def isApprove(self, session):
        return session.post(self.isApprove_url)


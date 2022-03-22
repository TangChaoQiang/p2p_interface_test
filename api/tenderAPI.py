import requests

import app


class tenderAPI():

    def __init__(self):
        self.session = requests.session()
        self.tender_url = app.Base_url + "/trust/trust/tender"
        self.mytenderlist_url = app.Base_url + "/loan/tender/mytenderlist"
        self.risk_appraisal_url = app.Base_url + "/risk/answer/submit"

    def tender(self, session, id="1863", depositCertificate= "-1", amount="100"):
        data = {"id": id, "depositCertificate": depositCertificate, "amount": amount}
        return session.post(url=self.tender_url, data=data)

    def mytenderlist(self, session, status):
        data = {"status": status}
        return session.post(url=self.mytenderlist_url, data=data)

    def risk_appraisal(self, session):
        data = {
            "answers_1": "b",
            "answers_2": "d",
            "answers_3": "a",
            "answers_4": "c",
            "answers_5": "c",
            "answers_6": "b",
            "answers_7": "a",
            "answers_8": "d",
            "answers_9": "b",
            "answers_10": "a"
        }
        return session.post(url=self.risk_appraisal_url, data=data)
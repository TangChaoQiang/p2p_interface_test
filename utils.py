import json
import logging
import requests, pymysql
from bs4 import BeautifulSoup

import app


def assert_utils(self, response, status_code, status, desc):
    self.assertEqual(response.status_code, status_code)
    self.assertEqual(response.json().get("status"), status)
    self.assertEqual(response.json().get("description"), desc)

def third_requests(self, form_data):
    # 定义Beautiful对象
    soup = BeautifulSoup(form_data, "html.parser")
    # 获取第三方接口的URL地址
    third_url = soup.form['action']
    logging.info("get response = {}".format(third_url))
    # 定义字典获取参数值
    data = {}
    for i in soup.find_all('input'):
        data.setdefault(i["name"], i["value"])
    # 发送请求
    response = requests.post(third_url, data=data)
    return response


class DB_mysql:
    @classmethod
    def get_conn(cls, db_name):
        conn = pymysql.connect(host=app.DB_URL, port=3306, user=app.DB_username, password=app.DB_password, db=db_name, autocommit=True)
        return conn

    @classmethod
    def close(cls, cursor, conn):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def delete(cls, db_name, sql):
        try:
            conn = cls.get_conn(db_name)
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close(cursor, conn)

def read_Imgcode_data(filename):
    file = app.base_dir + "/data/" + filename
    test_data = []
    with open(file, encoding='utf-8') as f:
        data = json.load(f)
        list_data = data.get("get_imgcode")
        for test_list_data in list_data:
            test_data.append((test_list_data.get("type"), test_list_data.get("status_code")))
    print("json data = {}".format(test_data))
    return test_data
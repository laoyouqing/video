import requests
import json


class YunPian(object):

    def __init__(self):
        self.secret_key = 'a6d6e990-273b-5fad-a0c1-7845ef1cde5b'
        self.single_send_url = "http://47.112.126.133:8004/push/"
        self.template_code= 'SMS_125020249'


    def send_sms(self, code, mobile):

        # 需要传递的参数
        params = {
            "secret_key": self.secret_key,
            "mobile": mobile,
            "msg": code,
            'template_code':self.template_code
        }

        response = requests.post(self.single_send_url, data=params)
        re_dict = json.loads(response.text)
        return re_dict
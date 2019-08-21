import json
from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen

import requests

from video import settings


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


# 授权
class WxOAuth(object):
    '''微信认证辅助工具类'''

    def __init__(self):
        self.appid = settings.APPID
        self.secret = settings.SECRET

    def get_access_token(self,code):
        print(self.appid, self.secret, code)
        req = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (self.appid, self.secret,code))
        print(req.text)
        access_token = json.loads(req.text)['access_token']
        openid = json.loads(req.text)['openid']
        if not (access_token or openid):
            raise Exception
        return (access_token,openid)

    def flush_access_token(self,refresh_token):
        req = requests.get('https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=%s&grant_type=refresh_token&refresh_token=%s' % (self.appid, refresh_token))
        # print(req.text)
        access_token = json.loads(req.text)['access_token']
        openid = json.loads(req.text)['openid']

        if not (access_token or openid):
            raise Exception
        return (access_token, openid)


    def get_user_info(self,access_token,openid):
        req = requests.get('https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN ' % (access_token, openid))
        req=req.content.decode('utf8')
        req=json.loads(req)
        openid = req.get('openid')
        nickname = req.get('nickname')
        headimgurl = req.get('headimgurl')
        sex = req.get('sex')
        if not (nickname or openid or headimgurl):
            raise Exception
        return (openid,nickname,headimgurl,sex)

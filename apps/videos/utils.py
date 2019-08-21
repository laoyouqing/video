import json
import requests

def get_accesstoken(appid,secret):
    req = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(appid,secret))
    token = json.loads(req.text)['access_token']
    return token

def get_jsapi_ticket(access_token):
    req = requests.get('https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi'%(access_token))
    ticket = json.loads(req.text)['ticket']
    return ticket
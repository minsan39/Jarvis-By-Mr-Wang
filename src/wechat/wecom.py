import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WeComBot:
    def __init__(self):
        self.corp_id = os.getenv("WECOM_CORP_ID")
        self.agent_id = os.getenv("WECOM_AGENT_ID")
        self.secret = os.getenv("WECOM_SECRET") 
        self.access_token = self.get_access_token()
    def get_access_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": self.corp_id,
            "corpsecret": self.secret
        }
        resp=requests.get(url,params=params)
        data = resp.json()
        if data["errcode"] == 0:
            self.access_token = data["access_token"]
            return self.access_token
        else:
            raise None
    
    def send_message(self,user_id:str,content:str)->bool:
        if not self.access_token:
            self.get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
        params = {
            "access_token": self.access_token,
        }
        payload = {
            "touser": user_id,
            "agentid": self.agent_id,
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        resp=requests.post(url,params=params,json=payload)
        data = resp.json()
        return data["errcode"] == 0
            




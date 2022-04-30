from datetime import datetime, timedelta, timezone
import hashlib
from lib2to3.pgen2 import token
from lib2to3.pgen2.tokenize import TokenError
from os import stat
from pydoc import plain
from Crypto.Cipher import AES
from pyparsing import java_style_comment
import requests,json
import time


#bytes to hex
def b2h(b):
    return ''.join([hex(b)[2:].zfill(2) for b in b])

#hex to bytes
def h2b(h):
    return bytes.fromhex(h)

def AES_Encrypt(text):
    ckey = '23DbtQHR2UMbH6mJ'
    # padding算法
    BS = len(ckey)
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    cryptor = AES.new(ckey.encode("utf8"),AES.MODE_ECB)
    ciphertext = cryptor.encrypt(bytes(pad(text), encoding="utf8"))
    return b2h(ciphertext).upper()


def AES_Decrpt(text):
    ckey = '23DbtQHR2UMbH6mJ'
    unpad = lambda s: s[0:-ord(s[-1:])]
    decode = h2b(text)
    cryptor = AES.new(ckey.encode("utf8"),AES.MODE_ECB)
    return unpad(cryptor.decrypt(decode)).decode('utf-8')

def getMD5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()


##################################
##                             ###
##      初始化参数              ###
##                            ###
#################################


#基本信息
account:str = '1111111111111'#手机号
password:str = 'xxx'#密码
address = "省份 · 地级市 · xx小区"#改成你的坐标
province = "所在省份"
city = "所在城市"
#经纬度最好抓包填上 不填也行
latitude =""
longitude=""





Accept_Language="zh-CN,zh;q=0.8"
user_agent_value="Mozilla/5.0 (Linux; U; Android 10; zh-cn; GLK-AL00 Build/HUAWEIGLK-AL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"
Content_Type="application/json; charset=UTF-8"
Host="api.moguding.net:9000"
Accept_Encoding=""
Cache_Control="no-cache"


state = ""

if datetime.utcnow().astimezone(timezone(timedelta(hours=8))).hour < 12:
    state = "START"
else:
    state = "END"

planIdURL = 'https://api.moguding.net:9000/practice/plan/v3/getPlanByStu'
signInURL = "https://api.moguding.net:9000/attendence/clock/v2/save"
#最新的v3接口 需要搭配clock使用
loginURL  = "https://api.moguding.net:9000/session/user/v3/login"

loginJson = {"password":AES_Encrypt(password),"t":AES_Encrypt(str(int(round(time.time()*1000)))),"phone":AES_Encrypt(account),"loginType":"android","uuid":""}
print("新版蘑菇钉的loginJson = ",loginJson)
res = requests.post(loginURL,
    headers={"Authorization":"","roleKey":"","Sign":"","Accept-Language":Accept_Language,"User-Agent":user_agent_value,"Content-Type":Content_Type,"Host":Host,"Accept-Encoding":Accept_Encoding,"Cache-Control":Cache_Control
    },
    json=loginJson)


UserId = res.json().get("data").get("userId")
Token = res.json().get("data").get("token")
sign = getMD5(str(UserId)+"student" + "3478cbbc33f84bd00d75d7dfa69e0daa")

res_plan = requests.post(planIdURL,headers={"Authorization":Token,"roleKey":"student","Sign":sign,"Accept-Language":Accept_Language,"User-Agent":user_agent_value,"Content-Type":Content_Type,"Host":Host,"Accept-Encoding":Accept_Encoding,"Cache-Control":Cache_Control
    },json={"state":""})

planID= json.loads(res_plan.text)['data'][0]['planId']
newSign = getMD5("Android"+state+planID+UserId+address+"3478cbbc33f84bd00d75d7dfa69e0daa")
SignInJson = {
      "country" : "中国",
      "address" : address,
    "province" : province,
    "t": AES_Encrypt(str(int(round(time.time()*1000)))),
    "city" : city,
    "latitude" : latitude,
    "description" : "",
    "planId":planID,
    "type":state,
    "device" : "Android",
    "longitude" : longitude
}
res_login = requests.post(signInURL,
headers={"Authorization":Token,"roleKey":"student","Sign":newSign,"Accept-Language":Accept_Language,
"User-Agent":user_agent_value,"Content-Type":Content_Type,"Host":Host,"Accept-Encoding":Accept_Encoding,
"Cache-Control":Cache_Control
    },
json=SignInJson
)



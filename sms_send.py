#coding=utf-8

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
# 短信应用SDK AppID
appid = 1400  # SDK AppID是1400开头

# 短信应用SDK AppKey
appkey = ""

# 需要发送短信的手机号码

# 短信模板ID，需要在短信应用中申请
template_id = 7839  # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请

# 签名
sms_sign = ""  # NOTE: 这里的签名"腾讯云"只是一个示例，真实的签名需要在短信控制台中申请，另外签名参数使用的是`签名内容`，而不是`签名ID`
ssender = SmsSingleSender(appid, appkey)
 # 当模板没有参数时，`params = []`
def sender(phone_numbers,params):
    try:
        result = ssender.send_with_param(86, phone_numbers,
        template_id, params, sign=sms_sign, extend="", ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)

    return result

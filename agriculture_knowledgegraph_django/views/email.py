from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from agriculture_knowledgegraph_django_model.models import SYS_USER, SYS_USER_IP, SYS_USER_FEEDBACK, SYS_USER_NAME, \
    SYS_LOG, SYS_USER_TOKEN, SYS_EMAIL_CODE
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from agriculture_knowledgegraph_django.utils import base64AesDecrypt, codeEncrypt, sendEmailAgri
from datetime import date
import json
import time
import random

# 锦满


@csrf_exempt
def sendEmailVerification(request):
    """
    函数名：sendEmailVerification
    功能：记录向邮箱发送的链接信息，并写入邮箱验证码表
    参数：
        request: 请求参数，包含邮箱、类型和附加信息
    返回值：
        success: 邮件是否发送成功
        log: 日志信息
    """
    # 获取邮箱、类型和附加信息
    if request.method == "POST":
        email = request.POST.get('email')
        type = int(request.POST.get('type'))
        msg = request.POST.get('msg')
        print("注册邮箱号：", base64AesDecrypt(email))
    else:
        return json_response({"success": False, "log": "request_is_not_post"})

    # 生成6位随机数验证码
    code = random.randint(100000, 999999)

    # 邮箱解密
    email = base64AesDecrypt(email)

    # 写入邮箱验证码表
    # 若不存在该邮箱，则在邮箱验证码表写入入参信息
    # 若已存在该邮箱，则用入参信息更新邮箱验证码表
    # 返回参数log按照子接口log返回信息

    query = SYS_EMAIL_CODE.objects.filter(ID=email)
    if query.exists():
        # 已存在该邮箱
        query.update(CODE=code, TYPE=type, MSG=msg,
                     SEND_TIMESTAMP=time.time()*1000)
    else:
        # 不存在该邮箱
        SYS_EMAIL_CODE.objects.create(
            ID=email, CODE=code, TYPE=type, MSG=msg, SEND_TIMESTAMP=time.time()*1000)

    # 根据tupe发送请求
    if type == 0:
        # 注册邮箱
        return accountRegistration(email, code)
    elif type == 1:
        # 注销邮箱
        return accountCancellation(email, code)
    elif type == 2:
        # 忘记密码
        return forgetPassword(email, code)
    else:
        # 更新邮箱
        return updateUserEmail(email, code)


@csrf_exempt
def verifyEmailCode(request):
    """
    函数名：verifyEmailCode
    功能：验证邮箱链接请求，并执行相关操作
    参数：
        request: 请求参数，包含邮箱和验证码
    返回值：
        success: 是否验证成功
        log: 日志信息
    """
    # 获取邮箱和验证码
    if request.method == "POST":
        email = request.POST.get('email')
        vcode = request.POST.get('vcode')
        msg = request.POST.get('msg')
    else:
        return json_response({"success": False, "log": "request_is_not_post"})

    # 邮箱验证码解密
    email = base64AesDecrypt(email)
    vcode = base64AesDecrypt(vcode)

    query = SYS_EMAIL_CODE.objects.filter(ID=email, CODE=vcode)
    if query.exists():
        # 已存在该邮箱
        if time.time() * 1000 - float(query.first().SEND_TIMESTAMP) <= 60 * 5 * 1000:
            if query.first().TYPE == 0:

                id = SYS_USER.objects.aggregate(Max('ID'))+1
                # 未超过5分钟
                SYS_USER.objects.create(
                    ID=id,
                    LOGIN_NAME="xxx",
                    PASSWORD="123456",
                    USER_TYPE=1,
                    SEX=1,
                    BORN_TIME=date.today,
                    CREATE_TIME=date.today,
                    ERROR_COUNT=0,
                    STATUS=0,
                    LOCK_TIME=0,
                    OCCUPATION="xxx",
                    EMAIL=email,
                    AVATAR="xxx"
                )
            elif query.first().TYPE == 1:
                SYS_USER.objects.filter(EMAIL=email).delete()
            elif query.first().TYPE == 2:
                SYS_USER.objects.filter(EMAIL=email).update(PASSWORD=msg)
            else:
                SYS_USER.objects.filter(EMAIL=email).update(EMAIL=msg)
            
            return json_response({"success": True, "log": "success"})
        else:
            return json_response({"success": False, "log": "exceed_5_minutes"})
    else:
        return json_response({"success": False, "log": "email_not_find"})
    


@csrf_exempt
def accountRegistration(email, code):
    """
    函数名：accountRegistration
    功能：向邮箱发送注册链接
    参数：
        request: 请求参数，包含邮箱
    返回值：
        success: 邮件是否发送成功
        vcode: 验证码
        log: 日志信息
    """

    # 发送包含验证信息的网页链接到邮箱
    # 返回参数log按照子接口log返回信息
    query = SYS_USER.objects.filter(EMAIL=email)
    if query.exists():
        # 已存在该邮箱
        return json_response({"success": False, "log": "email_already_exist"})
    else:
        link = codeEncrypt(code, email)
        success = sendEmailAgri(email, link, 0)
        if success:
            # 发送成功
            return json_response({"success": True, "log": "success"})
        else:
            return json_response({"success": False, "log": "fail_to_connect_server"})


@csrf_exempt
def accountCancellation(email, code):
    """
    函数名：accountCancellation
    功能：向邮箱发送注销链接
    参数：
        request: 请求参数，包含邮箱
    返回值：
        success: 邮件是否发送成功
        vcode: 验证码
        log: 日志信息
    """

    # 发送包含验证信息的网页链接到邮箱
    # 返回参数log按照子接口log返回信息
    query = SYS_USER.objects.filter(EMAIL=email)
    if query.exists():
        # 已存在该邮箱
        link = codeEncrypt(code, email)
        success = sendEmailAgri(email, link, 1)
        if success:
            # 发送成功
            return json_response({"success": True, "log": "success"})
        else:
            # 发送失败
            return json_response({"success": False,  "log": "fail_to_connect_server"})
    else:
        # 不存在该邮箱
        return json_response({"success": False, "log": "email_not_exist"})


@csrf_exempt
def updateUserEmail(email, code):
    """
    函数名：updateUserEmail
    功能：向邮箱发送更新邮箱链接
    参数：
        request: 请求参数，包含邮箱
    返回值：
        success: 邮件是否发送成功
        vcode: 验证码
        log: 日志信息
    """

    # 发送包含验证信息的网页链接到邮箱
    # 返回参数log按照子接口log返回信息
    query = SYS_USER.objects.filter(EMAIL=email)
    if query.exists():
        # 已存在该邮箱
        link = codeEncrypt(code, email)
        success = sendEmailAgri(email, link, 3)
        if success:
            # 发送成功
            return json_response({"success": True, "log": "success"})
        else:
            # 发送失败
            return json_response({"success": False, "log": "fail_to_connect_server"})
    else:
        # 不存在该邮箱
        return json_response({"success": False, "log": "email_not_exist"})


@csrf_exempt
def forgetPassword(email, code):
    """
    函数名：forgetPassword
    功能：向邮箱发送忘记密码链接
    参数：
        request: 请求参数，包含邮箱
    返回值：
        success: 邮件是否发送成功
        vcode: 验证码
        log: 日志信息
    """

    # 发送包含验证信息的网页链接到邮箱
    # 返回参数log按照子接口log返回信息

    query = SYS_USER.objects.filter(EMAIL=email)
    if query.exists():
        # 已存在该邮箱
        link = codeEncrypt(code, email)
        success = sendEmailAgri(email, link, 2)
        if success:
            # 发送成功
            return json_response({"success": True, "log": "success"})
        else:
            # 发送失败
            return json_response({"success": False, "log": "fail_to_connect_server"})
    else:
        # 不存在该邮箱
        return json_response({"success": False, "log": "email_not_exist"})


@csrf_exempt
def json_response(answer):
    print(answer)
    return HttpResponse(json.dumps(answer, ensure_ascii=False))

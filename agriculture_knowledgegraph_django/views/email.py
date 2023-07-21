from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from agriculture_knowledgegraph_django_model.models import SYS_USER, SYS_USER_IP, SYS_USER_FEEDBACK, SYS_USER_NAME, \
    SYS_LOG, SYS_USER_TOKEN, SYS_EMAIL_CODE
from django.views.decorators.csrf import csrf_exempt
from agriculture_knowledgegraph_django.utils import aesDecrypt, codeEncrypt, sendEmailAgri
import json
import time
import random


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
    email = request['email']
    type = request['type']
    msg = request['msg']

    # 生成6位随机数验证码
    code = random.randint(100000, 999999)

    # 邮箱解密
    email = aesDecrypt(email)

    # 写入邮箱验证码表
    # 若不存在该邮箱，则在邮箱验证码表写入入参信息
    # 若已存在该邮箱，则用入参信息更新邮箱验证码表
    # 返回参数log按照子接口log返回信息
    query = SYS_EMAIL_CODE.objects.filter(ID=email)
    if query.exists():
        # 已存在该邮箱
        query.update(CODE=code, TYPE=type, MSG=msg,
                    SEND_TIMESTAMP=time.time()*1000)
        return {"success": True, "log": "F0001"}
    else:
        # 不存在该邮箱
        SYS_EMAIL_CODE.objects.create(
            ID=email, CODE=code, TYPE=type, MSG=msg, SEND_TIMESTAMP=time.time()*1000)
        return {"success": True, "log": "F0001"}


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
    email = request['email']
    vcode = request['vcode']

    # 邮箱验证码解密
    email = aesDecrypt(email)
    vcode = aesDecrypt(vcode)

    query = SYS_EMAIL_CODE.objects.filter(ID=email, CODE=vcode)
    if query.exists():
        # 已存在该邮箱
        if time.time() * 1000 - query.first().SEND_TIMESTAMP >= 60 * 5 * 1000:
            # 超过5分钟
            if query.first().TYPE == 0:
                # 注册邮箱
                accountRegistration(request)
                return {"success": True, "log": "F0001"}
            elif query.first().TYPE == 1:
                # 注销邮箱
                accountCancellation(request)
                return {"success": True, "log": "F0001"}
            elif query.first().TYPE == 2:
                # 忘记密码
                forgetPassword(request)
                return {"success": True, "log": "F0001"}
            else:
                # 更新邮箱
                updateUserEmail(request)
                return {"success": True, "log": "F0001"}
        else:
            return {"success": False, "log": "F0004"}
    else:
        return {"success": False, "log": "F0005"}


def accountRegistration(request):
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
    # 获取邮箱
    email = request['email']

    # 邮箱解密
    email = aesDecrypt(email)

    # 发送包含验证信息的网页链接到邮箱
    # 返回参数log按照子接口log返回信息
    query = SYS_EMAIL_CODE.objects.filter(ID=email)
    if query.exists():
        # 已存在该邮箱
        code = query.first().CODE
        link = codeEncrypt(code, email)
        success = sendEmailAgri(email, link, 0)
        if success:
            # 发送成功
            return {"success": True, "vcode": code, "log": "F0001"}
        else:
            # 发送失败
            return {"success": False, "vcode": code, "log": "F0002"}
    else:
        # 不存在该邮箱
        return {"success": False, "log": "F0002"}


def accountCancellation(request):
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
    # 获取邮箱
    email = request['email']

    # 邮箱解密
    email = aesDecrypt(email)

    # 发送包含验证信息的网页链接到邮箱
    # 返回参数log按照子接口log返回信息
    query = SYS_EMAIL_CODE.objects.filter(ID=email)
    if query.exists():
        # 已存在该邮箱
        code = query.first().CODE
        link = codeEncrypt(code, email)
        success = sendEmailAgri(email, link, 1)
        if success:
            # 发送成功
            return {"success": True, "vcode": code, "log": "F0001"}
        else:
            # 发送失败
            return {"success": False, "vcode": code, "log": "F0002"}
    else:
        # 不存在该邮箱
        return {"success": False, "log": "F0002"}


def updateUserEmail(request):
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
    # 获取邮箱
    email = request['email']

    # 邮箱解密
    email = aesDecrypt(email)

    # 发送包含验证信息的网页链接到邮箱
    # 返回参数log按照子接口log返回信息
    query = SYS_EMAIL_CODE.objects.filter(ID=email)
    if query.exists():
        # 已存在该邮箱
        code = query.first().CODE
        link = codeEncrypt(code, email)
        success = sendEmailAgri(email, link, 3)
        if success:
            # 发送成功
            return {"success": True, "vcode": code, "log": "F0001"}
        else:
            # 发送失败
            return {"success": False, "vcode": code, "log": "F0002"}
    else:
        # 不存在该邮箱
        return {"success": False, "log": "F0002"}


def forgetPassword(request):
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
    # 获取邮箱
    email = request['email']

    # 邮箱解密
    email = aesDecrypt(email)

    # 发送包含验证信息的网页链接到邮箱
    # 返回参数log按照子接口log返回信息
    query = SYS_EMAIL_CODE.objects.filter(ID=email)
    if query.exists():
        # 已存在该邮箱
        code = query.first().CODE
        link = codeEncrypt(code, email)
        success = sendEmailAgri(email, link, 2)
        if success:
            # 发送成功
            return {"success": True, "vcode": code, "log": "F0001"}
        else:
            # 发送失败
            return {"success": False, "vcode": code, "log": "F0002"}
    else:
        # 不存在该邮箱
        return {"success": False, "log": "F0002"}

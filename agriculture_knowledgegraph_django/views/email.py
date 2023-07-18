from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from agriculture_knowledgegraph_django_model.models import SYS_USER, SYS_USER_IP, SYS_USER_FEEDBACK, SYS_USER_NAME, \
    SYS_LOG, SYS_USER_TOKEN, SYS_EMAIL_CODE
import json
from django.views.decorators.csrf import csrf_exempt


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

    # 写入邮箱验证码表
    # 若不存在该邮箱，则在邮箱验证码表写入入参信息
    # 若已存在该邮箱，则用入参信息更新邮箱验证码表
    # 返回参数log按照子接口log返回信息
    pass


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

    pass


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

    # 发送包含验证信息的网页链接到邮箱
    # 返回参数log按照子接口log返回信息
    pass


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

    # 发送包含验证信息的网页链接到邮箱
    # 返回参数log按照子接口log返回信息
    pass


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

    # 发送包含验证信息的网页链接到邮箱
    # 返回参数log按照子接口log返回信息
    pass


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

    # 发送包含验证信息的网页链接到邮箱
    # 返回参数log按照子接口log返回信息
    pass
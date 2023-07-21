import sqlite3
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from agriculture_knowledgegraph_django_model.models import (
    SYS_USER,
    SYS_USER_IP,
    SYS_USER_FEEDBACK,
    SYS_USER_NAME,
    SYS_LOG,
    SYS_USER_TOKEN,
    SYS_EMAIL_CODE,
)
import json
import secrets
import string
from django.views.decorators.csrf import csrf_exempt
from agriculture_knowledgegraph_django.utils import base64AesDecrypt, base64AesEncrypt
import requests

# 水木
@csrf_exempt
def login(request):
    """
    函数名：login
    功能：用户登录
    参数：
        request: 请求参数，包含邮箱/ID、密码和token
    返回值：
        success: 是否验证成功
        content: 需要读取的内容
        log: 日志信息
    """
    if request.method == "POST":
        login = request.POST.get("login")
        is_id = request.POST.get("is_id")
        password = base64AesDecrypt(request.POST.get("password"))
        print(login, is_id, password)
    else:
        return json_response(
            {"success": False, "content": {}, "log": "fail_to_connect_server"}
        )

    # 更新随机token
    # 验证ID、密码和token
    try:
        if is_id == "true":
            is_id = True
        else:
            is_id = False

        if is_id:
            user = SYS_USER.objects.get(ID=login)
        else:
            user = SYS_USER.objects.get(EMAIL=login)

        if user.PASSWORD == password:
            success = True
            token = "".join(
                secrets.choice(string.ascii_letters + string.digits) for _ in range(16)
            )
            user_token = SYS_USER_TOKEN(ID=user.ID, TOKEN=token)
            user_token.save()
            data = {
                "id": user.ID,
                "token": token,
                "internal_access": True,
            }
            userMessage = json.loads(getUserMessage(data).content)
            userRealNameMessage = json.loads(getUserRealNameMessage(data).content)
            sitecontent = getUserIP(request)
            # # 输出解码后的信息
            # print(userMessage,userRealNameMessage)
            content = {**userMessage["content"], **userRealNameMessage["content"]}
            # content=''
            log = "succeed_to_login"
            return json_response(
                {
                    "success": success,
                    "content": content,
                    "token": token,
                    "log": log,
                    "site":sitecontent,
                }
            )

        else:
            success = False
            content = None
            log = "password_is_incorrect"

    except SYS_USER.DoesNotExist:
        success = False
        content = None
        if is_id:
            log = "ID_not_exist"
        else:
            log = "mailbox_not_exist"

    return json_response(
        {
            "success": success,
            "content": content,
            "log": log,
        }
    )


@csrf_exempt
def getUserRealNameMessage(request):
    """
    函数名：getUserRealNameMessage
    功能：获取用户实名信息
    参数：
        request: 请求参数，包含ID和token
    返回值：
        success: 是否验证成功
        content: 需要读取的内容
        log: 日志信息
    """
    try:
        if request["internal_access"] == True:
            id = request["id"]
            token = request["token"]
    except:
        # 获取ID和token
        if request.method == "POST":
            id = request.POST.get("id")
            token = base64AesDecrypt(request.POST.get("token"))
        else:
            return json_response(
                {"success": False, "content": {}, "log": "fail_to_connect_server"}
            )

    # 比对id和token的值
    try:
        user_token = SYS_USER_TOKEN.objects.get(ID=id, TOKEN=token)
    except SYS_USER_TOKEN.DoesNotExist:
        return json_response(
            {"success": False, "content": {}, "log": "invalid_id_or_token"}
        )

    # 读取用户实名信息
    try:
        user_name = SYS_USER_NAME.objects.get(ID=user_token.ID)
        user_info = {
            "name": base64AesEncrypt(user_name.NAME),
            "tel": base64AesEncrypt(user_name.TEL),
            "card_type": base64AesEncrypt(user_name.CARD_TYPE),
            "id_card": base64AesEncrypt(user_name.IDCARD),
        }
        return json_response(
            {
                "success": True,
                "content": user_info,
                "log": "succeed_to_get_User_real_name_message",
            }
        )
    except SYS_USER_NAME.DoesNotExist:
        return json_response({"success": False, "content": {}, "log": "ID_not_exise"})


@csrf_exempt
def getUserMessage(request):
    """
    函数名：getUserMessage
    功能：获取用户基础信息
    参数：
        request: 请求参数，包含ID和token
    返回值：
        success: 是否验证成功
        content: 需要读取的内容
        log: 日志信息
    """
    # 获取ID和token
    try:
        if request["internal_access"] == True:
            id = request["id"]
            token = request["token"]
    except:
        # 获取ID和token
        if request.method == "POST":
            id = request.POST.get("id")
            token = base64AesDecrypt(request.POST.get("token"))
        else:
            return json_response(
                {"success": False, "content": {}, "log": "fail_to_connect_server"}
            )

    # 比对id和token的值
    try:
        user_token = SYS_USER_TOKEN.objects.get(ID=id, TOKEN=token)
    except SYS_USER_TOKEN.DoesNotExist:
        return json_response(
            {"success": False, "content": {}, "log": "invalid_id_or_token"}
        )
    # 读取用户基本信息
    try:
        user_name = SYS_USER.objects.get(ID=user_token.ID)
        user_info = {
            "id":id,
            "login_name": user_name.LOGIN_NAME,
            "user_type": user_name.USER_TYPE,
            "sex": user_name.SEX,
            "born_time": user_name.BORN_TIME,
            "create_time": user_name.CREATE_TIME,
            "error_count": user_name.ERROR_COUNT,
            "status": user_name.STATUS,
            "lock_time": user_name.LOCK_TIME,
            "occupation": user_name.OCCUPATION,
            "email": user_name.EMAIL,
            "avatar": user_name.AVATAR,
        }
        return json_response({"success": True, "content": user_info, "log": "success"})
    except SYS_USER.DoesNotExist:
        return json_response({"success": False, "content": {}, "log": "ID_not_exist"})


@csrf_exempt
def updateAcountInformation(request):
    """
    函数名：updateAcountInformation
    功能：更新用户基础信息
    参数：
        request: 请求参数，包含ID、token和更新的信息
    返回值：
        success: 是否验证成功
        log: 日志信息
    """
    # 获取ID、token和更新的信息
    if request.method == "POST":
        id = request.POST.get("id")
        token = base64AesDecrypt(request.POST.get("token"))
        sex = request.POST.get("sex")
        occupation = request.POST.get("occupation")
        born_time = request.POST.get("born_time")
    else:
        return json_response(
            {"success": False, "content": {}, "log": "fail_to_connect_server"}
        )

        # 比对id和token的值
    try:
        user_token = SYS_USER_TOKEN.objects.get(ID=id, TOKEN=token)
    except SYS_USER_TOKEN.DoesNotExist:
        return json_response(
            {"success": False, "content": {}, "log": "invalid_id_or_token"}
        )
    # 更新用户基础信息
    user = SYS_USER.objects.get(ID=id)
    user.SEX = sex
    user.OCCUPATION = occupation
    user.BORN_TIME = born_time
    user.save()
    return json_response(
        {"success": True, "content": {}, "log": "update-account-information-success"}
    )


@csrf_exempt
def updateUserPassword(request):
    """
    函数名：updateUserPassword
    功能：更新用户密码
    参数：
        request: 请求参数，包含邮箱/ID、旧密码、新密码和token
    返回值：
        success: 是否验证成功
        log: 日志信息
    """

    if request.method == "POST":
        login = request.POST.get("login")
        is_id = request.POST.get("is_id")
        old_password = base64AesDecrypt(request.POST.get("old_password"))
        new_password = base64AesDecrypt(request.POST.get("new_password"))
        token = base64AesDecrypt(request.POST.get("token"))
    else:
        return json_response(
            {"success": False, "content": {}, "log": "fail_to_connect_server"}
        )

    # 验证邮箱/ID、旧密码和token
    try:
        if is_id == "true":
            is_id = True
        else:
            is_id = False
        if is_id:
            user = SYS_USER.objects.get(ID=login)

        else:
            user = SYS_USER.objects.get(EMAIL=login)

        try:
            user_token = SYS_USER_TOKEN.objects.get(ID=user.ID, TOKEN=token)
        except SYS_USER_TOKEN.DoesNotExist:
            return json_response(
                {"success": False, "content": {}, "log": "invalid_id_or_token"}
            )

        if user.PASSWORD == old_password:
            user.PASSWORD = new_password
            user.save()
            success = True
            content = None
            log = "success_to_change_password"

        else:
            success = False
            content = None
            log = "password_is_incorrect"

    except SYS_USER.DoesNotExist:
        if is_id == "false":
            success = False
            content = None
            log = "mailbox_not_exist"
        else:
            success = False
            content = None
            log = "ID_not_exise"
    # 更新密码
    # 返回参数log
    return json_response({"success": success, "content": content, "log": log})


@csrf_exempt
def updateUserRealNameMessage(request):
    """
    函数名：updateUserRealNameMessage
    功能：更新用户实名信息
    参数：
        request: 请求参数，包含ID、token和更新的实名信息
    返回值：
        success: 是否验证成功
        log: 日志信息
    """
    # 获取ID、token和更新的实名信息
    if request.method == "POST":
        id = request.POST.get("id")
        token = base64AesDecrypt(request.POST.get("token"))
        name = request.POST.get("name")
        tel = request.POST.get("tel")
        card_type = request.POST.get("card_type")
        id_card = request.POST.get("id_card")
    else:
        return json_response(
            {"success": False, "content": {}, "log": "fail_to_connect_server"}
        )

    # 验证ID和token

    try:
        user_token = SYS_USER_TOKEN.objects.get(ID=id, TOKEN=token)
    except SYS_USER_TOKEN.DoesNotExist:
        return json_response(
            {"success": False, "content": {}, "log": "invalid_id_or_token"}
        )

    # 更新用户基础信息
    user = SYS_USER_NAME.objects.get(ID=id)
    user.NAME = name
    user.TEL = tel
    user.CARD_TYPE = card_type
    user.IDCARD = id_card
    user.save()
    return json_response(
        {"success": True, "content": {}, "log": "update-account-information-success"}
    )


@csrf_exempt
def deleteUserRealNameMessage(request):
    """
    函数名：deleteUserRealNameMessage
    功能：删除用户实名信息
    参数：
        request: 请求参数，包含ID和token
    返回值：
        success: 是否验证成功
        log: 日志信息
    """
    if request.method == "POST":
        id = request.POST.get("id")
        token = base64AesDecrypt(request.POST.get("token"))
    else:
        return json_response(
            {"success": False, "content": {}, "log": "fail_to_connect_server"}
        )

    # 验证ID和token
    try:
        user_token = SYS_USER_TOKEN.objects.get(ID=id, TOKEN=token)
    except SYS_USER_TOKEN.DoesNotExist:
        return json_response(
            {"success": False, "content": {}, "log": "invalid_id_or_token"}
        )

    # 更新用户基础信息
    user = SYS_USER_NAME.objects.get(ID=id)
    user.delete()
    user.save()
    return json_response(
        {"success": True, "content": {}, "log": "delete-account-information-success"}
    )

    # 删除用户实名信息
    # 返回参数log


# ShmilAyu
# X-Forwarded-For:简称XFF头，它代表客户端，也就是HTTP的请求端真实的IP，只有在通过了HTTP 代理或者负载均衡服务器时才会添加该项。
def getUserIP(request):
    """获取请求者的IP信息"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get("REMOTE_ADDR")  # 未使用代理获取IP
    url = "https://api.vvhan.com/api/getIpInfo?ip="+str(ip)
    response =requests.get(url)
    if response.status_code==200:
        content=json.loads(response.content)
        print(content)
        if content["success"]==True:
            city=content["info"]["city"]
        else:
            city="未知"
    else:
        city="未知"
    res={"ip":ip,"city":city}
    return res


def updateUserIP(request):
    """
    函数名：updateUserIP
    功能：更新用户IP地址
    参数：
        request: 请求参数，包含ID和token
    返回值：
        success: 是否验证成功
        log: 日志信息
    """
    # 获取ID和token
    if request.method == "POST":
        id = request.POST.get("id")
        token = base64AesDecrypt(request.POST.get("token"))
    else:
        print(request.method)
        return json_response({"success": False, "log": "fail_to_connect_server"})
    ip = getUserIP(request)["ip"]
    # 更新用户IP地址表
    # 返回参数log
    try:
        SYS_USER_TOKEN.objects.get(ID=id, TOKEN=token)
    except SYS_USER_TOKEN.DoesNotExist:
        return json_response(
            {"success": False, "content": {}, "log": "invalid_id_or_token"}
        )
    try:
        feedback = SYS_USER_IP.objects.get(ID=id)
        # print("1:"+feedback.IP)
        # print("2:"+ip)
        feedback.IP = ip
        feedback.save()
        return json_response({"success": True, "log": "success"})
    except SYS_USER.DoesNotExist:
        # print("提交失败")
        return json_response({"success": False, "log": "fail_to_connect_server"})

#ShmilAyu
def userFeedback(request):
    """
    函数名：userFeedback
    功能：提交用户反馈意见或bug
    参数：
        request: 请求参数，包含ID、token、类型、文字信息和图片
    返回值：
        success: 是否验证成功
        log: 日志信息
    """
    # 获取ID、token、类型、文字信息和图片
    if(request.method=="POST"):
        id = request.POST.get('id')
        token = request.POST.get('token')
        type = request.POST.get('type')
        msg = request.POST.get('msg')
        img_0 = sqlite3.Binary(request.POST.get('img_0'))
        img_1 = sqlite3.Binary(request.POST.get('img_1'))
        img_2 = sqlite3.Binary(request.POST.get('img_2'))
        img_3 = sqlite3.Binary(request.POST.get('img_3'))
    else:
        return json_response({"success": False, "log": "fail_to_connect_server"})
    # 提交用户反馈意见或bug
    # 返回参数log
    try:
        user_token = SYS_USER_TOKEN.objects.get(ID=id, TOKEN=token)
    except SYS_USER_TOKEN.DoesNotExist:
        return json_response({"success": False, "content": {}, "log": "invalid_id_or_token"})
    try:
        feedback = SYS_USER_FEEDBACK(ID=id, CREATE_TIME=int(time.time()), TYPE=type, MSG=msg,
                                     IMG_0=img_0, IMG_1=img_1, IMG_2=img_2, IMG_3=img_3)
        feedback.save()
        # print(feedback)
        # print("提交成功")
        return json_response({"success": True, "log": "success"})

    except SYS_USER_FEEDBACK.DoesNotExist:
        # print("提交失败")
        return json_response({"success": False, "log": "fail_to_connect_server"})

def avatarSubmission(request):
    """
    函数名：avatarSubmission
    功能：提交用户头像
    参数：
        request: 请求参数，包含ID、token和头像
    返回值：
        success: 是否验证成功
        log: 日志信息
    """
    # 获取ID、token和头像
    if request.method=="POST":
        id = request.POST.get('id')
        token = base64AesDecrypt(request.POST.get('token'))
        avatar = sqlite3.Binary(request.POST.get('avatar'))
    else:
        print(request.method)
        return json_response({"success": False, "log": "fail_to_connect_server"})
    # 比对id和token的值
    # 存储用户数据库头像信息
    # 返回参数log
    try:
        SYS_USER_TOKEN.objects.get(ID=id, TOKEN=token)
    except SYS_USER_TOKEN.DoesNotExist:
        return json_response({"success": False, "content": {}, "log": "invalid_id_or_token"})
    try:
        feedback = SYS_USER.objects.get(ID=id)
        feedback.AVATAR=avatar
        feedback.save()
        return json_response({"success": True, "log": "success"})

    except SYS_USER.DoesNotExist:
        # print("提交失败")
        return json_response({"success": False, "log": "fail_to_connect_server"})

def updateUserIP(request):
    """
    函数名：updateUserIP
    功能：更新用户IP地址
    参数：
        request: 请求参数，包含ID和token
    返回值：
        success: 是否验证成功
        log: 日志信息
    """
    # 获取ID和token
    if request.method=="POST":
        id = request.POST.get('id')
        token =base64AesDecrypt(request.POST.get('token'))
    else:
        print(request.method)
        return json_response({"success": False, "log": "fail_to_connect_server"})
    ip =getUserIP(request)
    # 更新用户IP地址表
    # 返回参数log
    try:
        SYS_USER_TOKEN.objects.get(ID=id, TOKEN=token)
    except SYS_USER_TOKEN.DoesNotExist:
        return json_response({"success": False, "content": {}, "log": "invalid_id_or_token"})
    try:
        feedback = SYS_USER_IP.objects.get(ID=id)
        # print("1:"+feedback.IP)
        # print("2:"+ip)
        feedback.IP=ip
        feedback.save()
        return json_response({"success": True, "log": "success"})
    except SYS_USER.DoesNotExist:
        # print("提交失败")
        return json_response({"success": False, "log": "fail_to_connect_server"})


def json_response(answer):
    print(answer)
    return HttpResponse(json.dumps(answer, ensure_ascii=False))

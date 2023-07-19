from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from agriculture_knowledgegraph_django_model.models import SYS_USER,SYS_USER_IP,SYS_USER_FEEDBACK,SYS_USER_NAME,SYS_LOG,SYS_USER_TOKEN,SYS_EMAIL_CODE
import json
import secrets
import string
from django.views.decorators.csrf import csrf_exempt

#水木
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
        login = request.POST.get('login')
        is_id = request.POST.get('is_id')
        password = request.POST.get('password')
        print(request)
    else:
        return json_response({"success": False, "content":"","log": "method-is-not-POST"})
    # 获取邮箱/ID、密码和token
    # 更新随机token
    # 验证ID、密码和token
    try:
        if is_id:
            user = SYS_USER.objects.get(ID=login)
            
        else:
            user = SYS_USER.objects.get(EMAIL=login)
        
        if user.PASSWORD == password:
            success = True
            token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
            user_token = SYS_USER_TOKEN(ID=user, TOKEN=token)
            user_token.save()
            data = {
                'id': user.ID,
                'token': token,
                'internal_access':True,
            }
            userMessage = getUserMessage(data)
            userRealNameMessage= getUserRealNameMessage(data)
            # print(userMessage,userRealNameMessage)
            content = {**userMessage["content"], **userRealNameMessage["content"]} 
            log = "success"
            return json_response({
                'success': success,
                'content': content,
                'token':token,
                'log': log,
            })

        else:
            success = False
            content = None
            log = "密码错误"

    except SYS_USER.DoesNotExist:
        success = False
        content = None
        log = "用户不存在"

    return json_response({
        'success': success,
        'content': content,
        'log': log,
    })

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
        if request['internal_access']==True:
            id = request['id']
            token = request['token']
    except:
    #获取ID和token
        if request.method == "POST":
            id = request.POST.get('id')
            token = request.POST.get('token')
        else:
            return json_response({"success": False, content:"","log": "method-is-not-POST"})
    
    # 比对id和token的值
    try:
        user_token = SYS_USER_TOKEN.objects.get(ID=id, TOKEN=token)
    except SYS_USER_TOKEN.DoesNotExist:
        return json_response({"success": False, "content": "", "log": "invalid-id-or-token"})

    # 读取用户实名信息
    try:
        user_name = SYS_USER_NAME.objects.get(ID=user_token.ID)
        user_info = {
            "name": user_name.NAME,
            "tel": user_name.TEL,
            "card_type": user_name.CARD_TYPE,
            "id_card": user_name.IDCARD
        }
        return json_response({"success": True, "content": user_info, "log": "success"})
    except SYS_USER_NAME.DoesNotExist:
        return json_response({"success": False, "content": "", "log": "user-info-not-found"})

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
        if request['internal_access']==True:
            id = request['id']
            token = request['token']
    except:
    #获取ID和token
        if request.method == "POST":
            id = request.POST.get('id')
            token = request.POST.get('token')
        else:
            return json_response({"success": False, content:"","log": "method-is-not-POST"})
    
    # 比对id和token的值
    try:
        user_token = SYS_USER_TOKEN.objects.get(ID=id, TOKEN=token)
    except SYS_USER_TOKEN.DoesNotExist:
        return json_response({"success": False, "content": "", "log": "invalid-id-or-token"})
    # 读取用户基本信息
    try:
        user_name = SYS_USER.objects.get(ID=user_token.ID)
        user_info = {
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
        return json_response({"success": False, "content": "", "log": "user-info-not-found"})

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
    id = request['id']
    token = request['token']
    sex = request['sex']
    occupation = request['occupation']
    born_time = request['born_time']

    # 更新用户基础信息
    # 返回参数log
    pass

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
    # 获取邮箱/ID、旧密码、新密码和token
    login = request['login']
    is_id = request['is_id']
    old_password = request['old_password']
    new_password = request['new_password']
    token = request['token']

    # 验证邮箱/ID、旧密码和token
    # 更新密码
    # 返回参数log
    pass

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
    id = request['id']
    token = request['token']
    name = request['name']
    tel = request['tel']
    card_type = request['card_type']
    id_card = request['id_card']

    # 更新用户实名信息
    # 返回参数log
    pass

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
    # 获取ID和token
    id = request['id']
    token = request['token']

    # 删除用户实名信息
    # 返回参数log
    pass

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
    id = request['id']
    token = request['token']
    type = request['type']
    msg = request['msg']
    img_0 = request['img_0']
    img_1 = request['img_1']
    img_2 = request['img_2']
    img_3 = request['img_3']

    # 提交用户反馈意见或bug
    # 返回参数log
    pass

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
    id = request['id']
    token = request['token']
    avatar = request['avatar']

    # 存储用户数据库头像信息
    # 返回参数log
    pass

# X-Forwarded-For:简称XFF头，它代表客户端，也就是HTTP的请求端真实的IP，只有在通过了HTTP 代理或者负载均衡服务器时才会添加该项。
def getUserIP(request):
    '''获取请求者的IP信息'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip

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
    id = request['id']
    token = request['token']

    # 更新用户IP地址表
    # 返回参数log
    pass

def json_response(answer):
    print(answer)
    return HttpResponse(json.dumps(answer, ensure_ascii=False))
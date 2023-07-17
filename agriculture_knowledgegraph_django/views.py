from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from agriculture_knowledgegraph_django_model.models import SYS_USER,SYS_USER_IP,SYS_USER_FEEDBACK,SYS_USER_NAME,SYS_LOG,SYS_USER_TOKEN,SYS_EMAIL_CODE
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
    # 获取邮箱/ID、密码和token
    login = request['login']
    is_id = request['is_id']
    password = request['password']
    token = request['token']

    # 更新随机token
    # 验证ID、密码和token
    # 返回参数content和log
    pass

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
    id = request['id']
    token = request['token']

    # 返回参数content和log
    pass

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
    # 获取ID和token
    id = request['id']
    token = request['token']

    # 返回参数content和log
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

@csrf_exempt
def testSendMessage(request):
    print("调用")
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        # 在这里处理数据，做出相应的响应
        response_data = {'message': '已收到数据：' + input_text}
        print(response_data)
        # return response(response_data)
        return json_response(response_data)
    else:
        print({'message': '只支持 POST 请求'})
        return json_response({'message': '只支持 POST 请求'})
    
def json_response(answer):
    return HttpResponse(json.dumps(answer, ensure_ascii=False))

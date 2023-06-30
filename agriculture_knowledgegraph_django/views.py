from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from agriculture_knowledgegraph_django_model.models import SYS_USER,SYS_USER_IP,SYS_USER_FEEDBACK,SYS_USER_NAME,SYS_LOG,SYS_USER_TOKEN,SYS_EMAIL_CODE
import json
from django.views.decorators.csrf import csrf_exempt


def sendEmailVerification(request):
    # 获取验证码信息
    # 写入邮箱验证码表 P_SYS_EMAIL_CODE_W
    # 返回参数
    pass

def verifyEmailCode(request):
    # 获取对应验证码
    # 删除验证码
    # 加入 P_SYS_EMAIL_CODE_D
    pass

def accountRegistration(request):
    # 获取注册信息
    # 在用户表 SYS_USER 创建新的元组
    # 返回参数
    pass

def accountCancellation(request):
    # 账号注销的函数逻辑
    pass

def accountLogin(request):
    # 账号登录的函数逻辑
    pass

def updateAcountInformation(request):
    # 用户基础信息更新的函数逻辑
    pass

def updateUserPassword(request):
    # 用户密码更新的函数逻辑
    pass

def updateUserEmail(request):
    # 用户邮箱更新的函数逻辑
    pass

def updateUserIP(request):
    # IP地址更新的函数逻辑
    pass

def userFeedback(request):
    # 用户反馈意见或bug提交的函数逻辑
    pass

def avatarSubmission(request):
    # 头像提交的函数逻辑
    pass

def forgotPassword(request):
    # 找回密码的函数逻辑
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

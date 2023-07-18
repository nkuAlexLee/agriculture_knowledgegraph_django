from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from agriculture_knowledgegraph_django_model.models import SYS_USER, SYS_USER_IP, SYS_USER_FEEDBACK, SYS_USER_NAME, \
    SYS_LOG, SYS_USER_TOKEN, SYS_EMAIL_CODE
import json
from django.views.decorators.csrf import csrf_exempt


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
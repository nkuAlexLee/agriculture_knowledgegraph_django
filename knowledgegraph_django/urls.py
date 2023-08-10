"""
URL configuration for knowledgegraph_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from knowledgegraph_django.views.user import (
    login,
    getUserMessage,
    updateUserPassword,
    updateUserIP,
    userFeedback,
    avatarSubmission,
    getUserRealNameMessage,
    updateUserRealNameMessage,
    deleteUserRealNameMessage,
    updateAccountInformation,
)
from knowledgegraph_django.views.email import (
    forgetPassword,
    updateUserEmail,
    accountCancellation,
    accountRegistration,
    verifyEmailCode,
    sendEmailVerification,
)

from knowledgegraph_django.views.neo4j import (
    searchNode,
    recognizeNode,
    searchRelationshipBetween,
    getNodeDetail,
    getNodeResume,
    setEncyContent,
    setMapContent,
    getOverview,
)


from knowledgegraph_django.views.test import (
    testSendMessage,
)

from knowledgegraph_django.views.AI import (
    getGptAnswer,
)
from knowledgegraph_django.views.stockmessage import (
    getStockAnswer,
    getStocklistAnswer,
)
from agriculture_knowledgegraph_django.views.stockpredict import (
    stockpredict,
)
urlpatterns = [
    # 其他URL配置
    path('admin/', admin.site.urls),
    path('sendEmailVerification/', sendEmailVerification,
         name='send_email_verification'),
    path('verifyEmailCode/', verifyEmailCode, name='verify_email_code'),
    path('accountRegistration/', accountRegistration,
         name='account_registration'),
    path('accountCancellation/', accountCancellation,
         name='account_cancellation'),
    path('updateUserEmail/', updateUserEmail, name='update_user_email'),
    path('forgetPassword/', forgetPassword, name='forget_password'),
    path('login/', login, name='login'),
    path('getUserMessage/', getUserMessage, name='get_user_message'),
    path('updateAccountInformation/', updateAccountInformation,
         name='update_account_information'),
    path('updateUserPassword/', updateUserPassword, name='update_user_password'),
    path('updateUserIP/', updateUserIP, name='update_user_ip'),
    path('userFeedback/', userFeedback, name='user_feedback'),
    path('avatarSubmission/', avatarSubmission, name='avatar_submission'),
    path('getUserRealNameMessage/', getUserRealNameMessage,
         name='get_user_real_name_message'),
    path('updateUserRealNameMessage/', updateUserRealNameMessage,
         name='update_user_real_name_message'),
    path('deleteUserRealNameMessage/', deleteUserRealNameMessage,
         name='delete_user_real_name_message'),
    path('testSendMessage/', testSendMessage, name='test_send_message'),
    path('searchNode/', searchNode, name='searchNode'),
    path('recognizeNode/', recognizeNode, name='recognizeNode'),
    path('getNodeDetail/', getNodeDetail, name='getNodeDetail'),
    path('getNodeResume/', getNodeResume, name='getNodeResume'),
    path('searchRelationshipBetween/', searchRelationshipBetween,
         name='searchRelationshipBetween'),
    path('setEncyContent/', setEncyContent, name='setEncyContent'),
    path('setMapContent/', setMapContent, name='setMapContent'),
    path('getOverview/', getOverview, name='getOverview'),
    path('stockPredict/', stockpredict, name='stockPredict'),
    path("getGptAnswer/", getGptAnswer, name="get_gpt_answer"),
    path('getStockAnswer/', getStockAnswer, name='get_stock_answer,'),
    path('getStocklistAnswer/', getStocklistAnswer, name='get_stock_list_answer,')
]

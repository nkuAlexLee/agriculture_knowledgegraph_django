# models.py
from django.db import models
class SYS_USER(models.Model):
    ID = models.IntegerField(primary_key=True)
    LOGIN_NAME = models.CharField(max_length=100)
    PASSWORD = models.CharField(max_length=100)
    USER_TYPE = models.IntegerField()
    SEX = models.IntegerField(null=True)
    BORN_TIME = models.DateField(null=True)
    CREATE_TIME = models.IntegerField()
    ERROR_COUNT = models.IntegerField()
    STATUS = models.IntegerField()
    LOCK_TIME = models.IntegerField(null=True)
    OCCUPATION = models.CharField(max_length=10, null=True)
    EMAIL = models.CharField(max_length=30)
    AVATAR = models.BinaryField(null=True)

class SYS_USER_IP(models.Model):
    ID =  models.IntegerField(primary_key=True)
    CN_IP = models.CharField(max_length=30, null=True)
    FG_IP = models.CharField(max_length=30, null=True)
    IP = models.CharField(max_length=30)


class SYS_USER_FEEDBACK(models.Model):
    ID =  models.IntegerField(primary_key=True)
    CREATE_TIME = models.IntegerField()
    TYPE = models.CharField(max_length=10)
    MSG = models.TextField()
    IMG_0 = models.BinaryField(null=True)
    IMG_1 = models.BinaryField(null=True)
    IMG_2 = models.BinaryField(null=True)
    IMG_3 = models.BinaryField(null=True)

class SYS_USER_NAME(models.Model):
    ID =  models.IntegerField(primary_key=True)
    NAME = models.CharField(max_length=50)
    TEL = models.CharField(max_length=30)
    CARD_TYPE = models.CharField(max_length=10)
    IDCARD = models.CharField(max_length=50)

class SYS_LOG(models.Model):
    CREATE_TIME_PY = models.IntegerField(null=True)
    CREATE_TIME = models.DateField(null=True)
    ERROR = models.CharField(max_length=10, null=True)
    TYPE = models.CharField(max_length=10)
    MSG = models.CharField(max_length=100, null=True)
    USER_ID = models.IntegerField()

class SYS_USER_TOKEN(models.Model):
    ID = models.IntegerField(primary_key=True)
    TOKEN = models.CharField(max_length=16)

class SYS_EMAIL_CODE(models.Model):
    ID = models.CharField(max_length=30, primary_key=True)
    CODE = models.IntegerField()
    TYPE = models.CharField(max_length=10)
    MSG=models.CharField(max_length=100,null=True)
    SEND_TIMESTAMP = models.CharField(max_length=10)
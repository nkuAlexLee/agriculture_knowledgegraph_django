# smtplib - 连接邮箱服务器、登录邮箱
from email.header import Header       # 邮件主题
from email.mime.text import MIMEText        # 邮件正文
from email.mime.multipart import MIMEMultipart          # 提供邮件对象
import smtplib # 自带（好像
from Crypto.Cipher import AES # pip install pycryptodome
from binascii import b2a_hex, a2b_hex 
from Crypto import Random
import base64
from verify_email import verify_email # pip install verify-email
import time

# 关于AES加密配置
key = "ABCDEF0123456789"
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
# 关于AES加密配置


def aesEncrypt(data:str, key=key):
    '''
    AES的ECB模式加密方法
    :param key: **
    :param data:被加密字符串（明文）
    :return:密文
    '''
    key = key.encode('utf8')
    # 字符串补位
    data = pad(data)
    cipher = AES.new(key, AES.MODE_ECB)
    # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
    result = cipher.encrypt(data.encode())
    encodestrs = base64.b64encode(result)
    enctext = encodestrs.decode('utf8')
    return enctext


def aesDecrypt(data:str, key=key):
    '''
    :param key: **
    :param data: 加密后的数据（密文）
    :return:明文
    '''
    # print(data)
    key = key.encode('utf8')
    data = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_ECB)

    # 去补位
    text_decrypted = unpad(cipher.decrypt(data))
    text_decrypted = text_decrypted.decode('utf8')
    # print(text_decrypted)
    return text_decrypted

def base64AesEncrypt(data:str, key=key):
    return base64Encode(aesEncrypt(data, key))

def base64AesDecrypt(data:str, key=key):
    print(data)
    data = base64Decode(data)
    return aesDecrypt(data, key)

def base64Encode(str:str):
    return base64.b64encode(str.encode()).decode()


def base64Decode(str:str):
    return base64.b64decode(str.encode()).decode()

def sendEmail(email_addr:str, content:dict, type:str):
    '''发送邮件 type选填plain、html'''
    # 检查邮箱
    # 使用verify_email函数验证电子邮件
    print(email_addr)
    # verify = verify_email(email_addr)
    verify=True
    print(content)
    # 检查验证值是否为True
    if verify:
        sender = {
            "email":"264921247@qq.com",
            "key":"tdqijtppzbzocaeb",
            "sender":"264921247@qq.com <264921247@qq.com>"
        }
        # 1)连接邮箱服务器
        con = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 2)登录邮箱
        con.login(sender["email"], sender["key"])
        # 3.创建邮件
        # 1)创建邮件对象
        email = MIMEMultipart()
        # 2)设置主题、收件人信息、发件人信息
        # 标题
        email["Subject"] = Header(content["header"], "utf-8").encode()
        # 收件人
        email['To'] = email_addr
        # 发件人
        email['From'] = sender["sender"]
        # 3)设置邮件正文
        content = MIMEText(content["content"], type, "utf-8")
        # 将正文添加到邮件中
        email.attach(content)
        # 4.发送邮件
        con.sendmail(sender["email"], email_addr, email.as_string())
        # 5. 退出登录
        con.quit()
        return True
    else:
        return False


def sendEmailAgri(email: str, link: str, type: int):
    '''后端接口调用这个,type:0:注册;1:忘记密码;2:换绑邮箱'''
    methods = ["帐号注册操作", "重置密码操作", "换绑邮箱操作"]
    html = f"""
        <body>
            <div style="width: 100%;display: flex;justify-content: center;align-items: center;flex-direction: column;">
                <h1>农业知识图谱</h1>
                <h3>亲爱的用户</h3>
                <h3>请点击以下链接完成您的{methods[type]}。</h3>
                <a href="{link}">验证链接</a>
                <h3>此邮件为自动生成邮件，请勿回复。</h3>
            </div>
        </body>
    """
    return sendEmail(email, {"header":"农业知识图谱验证信息", "content":html}, "html")


def codeEncrypt(code:str, email:str):
    '''后端接口调用这个,完成对验证码的加密操作,返回发送链接 int(time.time()*1000)'''
    send_dict = {
        "vcode":code,
        "email":email,
        "timestamp":int(time.time()*1000)
    }
    send_dict = str(send_dict).replace("'", '"')
    send_dict = aesEncrypt(send_dict, key)
    send_dict = base64Encode(send_dict)
    link = f"http://localhost:8080/#/verify/{send_dict}"
    return link

if "__name__"=="__main__":
    code = "123456"
    to_email = "2112794@mail.nankai.edu.cn"
    link = codeEncrypt(code, to_email)
    success = sendEmailAgri("2112794@mail.nankai.edu.cn", link, 1)
    print(success) # True
    success = sendEmailAgri("211sadcadad2794@mail.nankai.edu.cn", link, 1)
    print(success) # False

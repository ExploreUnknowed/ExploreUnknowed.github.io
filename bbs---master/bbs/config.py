#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"
import  os
from datetime import timedelta
SECRET_KEY = "test_admin"
# PERMANENT_SESSION_LISFETIME = timedelta(days = 7)
DEBUG = True
# PERMANENT_SESSION_LIFETIME = True
# 查查这句bug 这个bug也是有很大的问题的d

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
PORT = '3306'
DATABASE = "bbs"
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
CMS_USER_ID = 'hello2020'
FRONT_USER_ID = 'hellohi'

# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
MAIL_USERNAME = '751439282@qq.com'
MAIL_PASSWORD = 'lzbnbhcbepldbbfb'
MAIL_DEFAULT_SENDER  = '751439282@qq.com'
# 配置mail 这个就可以是发送邮件了

# sorry，这个接口不能用了，那么就只能是换个接口了，不用这个了。。
ALIDAYU_APP_KEY = '23709557'
ALIDAYU_APP_SECRET = 'd9e430e0a96e21c92adacb522a905c4b'
ALIDAYU_SIGN_NAME = '小饭桌应用'
ALIDAYU_TEMPLATE_CODE = 'SMS_68465012'
# 这种采用session的方式也是一个小技巧，如果直接采用user_id，有可能就是重复了，如果后端采用一个CMS_USER_ID 这样的行为，相当于队这个变量重新赋值了。

# 采用uedtior编辑器的上传文件目录，这个是为帖子做准备的，其他的就不用了，直接是不用七牛云，直接是在本地存储
import  os
UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__) , 'static\content')
UEDITOR_UPLOAD_TO_QINIU = False
UEDITOR_QINIU_ACCESS_KEY = ""
UEDITOR_QINIU_SECRET_KEY = ""
UEDITOR_QINIU_BUCKET_NAME = ""
UEDITOR_QINIU_DOMAIN = ""

PER_PAGE = 10

# celeray配置redis
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"

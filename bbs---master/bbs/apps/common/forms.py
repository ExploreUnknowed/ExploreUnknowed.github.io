#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"
from apps.forms import BaseForm
from wtforms import  StringField
from wtforms.validators import regexp,InputRequired
import  hashlib

# 对验证码进行校验的类
class SMSCaptchaForm(BaseForm):
    salt = '12345623##$'

    sign = StringField(validators=[InputRequired()])

    # 从前端传过来的值，要进行解密，这个解密是写个方法，就是一个解密md5，其实这个md5只要知道盐，就可以知道这个原数据了
    def validate(self):
        result =  super(BaseForm ,self ).validate()
        if not result:
            return False
#         unicode默认是str类型，而hashlib 默认是byte类型，这个类型需要是进行改变，改变成utf-8类型的
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data
        # md5 = timestamp + telephone + sign 这是格式
        sign2 = hashlib.md5((timestamp + telephone + self.salt) .encode('utf-8'))
        if sign == sign2:
            return  True
        else:
            return False

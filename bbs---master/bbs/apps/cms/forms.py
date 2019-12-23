#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, InputRequired, Email, EqualTo
from wtforms import  ValidationError
from utils import zlcache
from flask import  g
from apps.forms import BaseForm

# 登录表单
class LoginForm(BaseForm):
    email = StringField(validators=[Email(), InputRequired()])
    password = StringField(validators=[Length(6, 20, message="请输入正确的密码 "), InputRequired(message="必须要输入一个密码")])
    rembmer = IntegerField()

    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message

#验证重置密码表单
class ResetForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='请输入正确格式的旧密码！')])
    newpwd = StringField(validators=[Length(6, 20, message='请输入正确格式的新密码！')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='确认密码必须和新密码一致！')])

#验证重置邮箱表单
class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的新邮箱')])
    captcha = StringField(validators=[Length(min=6, max=6, message='请输入正确长度的验证码!')])
    #写一个验证的方法
    def validate_captcha(self ,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = zlcache.get(email)
        # 要保证有验证码 要不然直接就等于了  再转换成小写 跟这个验证码的小写进行比对
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise  ValidationError("邮箱验证码错误")
    #如果两次邮箱都一样
    def validate_email(self , field):
        email = field.data
        user = g.cms_user
        if user.email == email :
            raise  ValidationError("不能修改为相同的邮箱")

# 添加板块表单验证
class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称！')])


# 更新板块表单验证
class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id！')])


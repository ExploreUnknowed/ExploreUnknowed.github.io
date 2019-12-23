#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"

from flask import  Blueprint,request
from exts import  alidayu
from utils import  restful
from utils.captcha import  Captcha
from .forms import  SMSCaptchaForm
bp = Blueprint('common' , __name__ ,url_prefix='/common')

@bp.route('/')
def index():
    return "cmmon index"


# 发送手机验证码,由于阿里大于这个接口出错，所以只能是放弃了
# @bp.route('/sms_captcha/')
# def sms_captcha():
    # telephone = request.args.get('telephone')
    # # 如果是错误的telephone
    # if not telephone:
    #     return restful.params_error(message="请传入正确的手机号码")
    #     # 如果是正确的，又该是这个样子
    # captcha = Captcha.gene_text(number=4)
    # if alidayu.send_sms('18339468991' , code = captcha):
    #     return restful.success()
    # else:
    #     return restful.params_error(message="短信验证码发送失败")
    #
    # form = SMSCaptchaForm(request.form)
    # if form.validate():
    #     telephone = form.telephone.data
    #     captcha = Captcha.gene_text(number=4)
    #     if alidayu.send_sms(telephone , code = captcha):
    #         print(captcha)
    #         return restful.success()
    #     else:
    #         return restful.params_error("短信验证码发送失败")
    # else:
    #     return restful.params_error("参数错误")




# @bp.route('/signup/')
# def signup():
#     return "hhh"


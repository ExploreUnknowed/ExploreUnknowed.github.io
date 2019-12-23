#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"
from .views import bp
from flask import session, g, render_template
from .models import FrontUser
import config


# 发送请求前传递前台用户
@bp.before_request
def before_request():
    if config.FRONT_USER_ID in session:
        user_id = session.get(config.FRONT_USER_ID)
        user = FrontUser.query.get(user_id)
        if user:
            g.front_user = user


# 404找不到页面钩子函数
@bp.errorhandler
def page_not_fount():
    return render_template('front/front_404.html'), 404

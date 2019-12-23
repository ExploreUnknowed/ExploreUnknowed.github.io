#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"
from functools import wraps
from flask import session, redirect, url_for, g
import config


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get(config.CMS_USER_ID):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))

    return inner


# 后台装饰器的问题，不写就暴漏接口了，可以进行修改
def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if g.cms_user.has_permissions(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.probfile'))

        return inner

    return outter
    # 装饰器在写的时候 容易出错，这个地方要注意，还有以后要多留意，留意装饰器的问题

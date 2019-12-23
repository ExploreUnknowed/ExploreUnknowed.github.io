#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"
from functools import wraps
from flask import session, redirect, url_for, g
import config

def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get(config.FRONT_USER_ID):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('front.signin'))

    return inner
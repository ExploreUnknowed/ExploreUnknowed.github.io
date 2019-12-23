#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"
from .views import bp
from flask import  session,g
from .modles import CmsUser,CMSPermission
import  config

@bp.before_request
def before_request():
    if session.get(config.CMS_USER_ID):
        user = CmsUser.query.get(session.get(config.CMS_USER_ID))
        if user:
            g.cms_user = user
            # 在写g对象的时候,也是有不一样的效果,这样的效果比较好,以后如果是多个用户的话,可以用__local__


# 添加一个上下文处理器
@bp.context_processor
def cms_context_processor():
    return {"CMSPermission" : CMSPermission}
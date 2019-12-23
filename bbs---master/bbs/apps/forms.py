#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"
from wtforms import Form


# 基础的表单验证类
class BaseForm(Form):
    def get_error(self):

        message = self.errors.popitem()[1][0]  # 需要返回什么信息视具体情况而定
        return message

    # 验证
    def validate(self):
        return super(BaseForm, self).validate()




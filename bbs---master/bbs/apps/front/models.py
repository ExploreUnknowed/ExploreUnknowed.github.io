#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"

from exts import db
import shortuuid, enum
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4

# 前台用户类，这个类可以是创建前台对象
class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)  # 使用shortuuid.uuid生成id
    telephone = db.Column(db.String(11), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)  # 密码比较特殊，需要加密
    email = db.Column(db.String(50), unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(FrontUser, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self._password, rawpwd)




#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"
from exts import db
from datetime import datetime
# 导入werkzug里面的md5值
from werkzeug.security import generate_password_hash, check_password_hash


# 管理权限模块
class CMSPermission(object):
    # 以二进制中255的方式来存储
    ALL_PERMISSION = 0b11111111
    # 权限的设置一个一个来
    # 匿名访问的权限
    VICTIOR = 0b00000001
    # 管理帖子的权限
    POSTER = 0b00000010
    # 管理评论的权限
    COMMENTER = 0b00000100
    # 管理板块的权限
    BOARDER = 0b00001000
    # 管理前台用户的权限
    FRONTUSER = 0b00010000
    # 管理后台的权限
    COMUSER = 0b0010000


# 权限和用户之间的中间表
cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True)
)


# 用户角色权限模型
class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # name代表的是角色
    name = db.Column(db.String(50), nullable=False)
    # desc是描述权限
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CMSPermission.VICTIOR)
    #     要跟用户进行一个绑定
    user = db.relationship('CmsUser', secondary=cms_role_user, backref='roles')



# cms 用户表
class CmsUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    datatime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    # 这种是为了防止直接拿到明文密码
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        res = check_password_hash(self.password, raw_password)
        return res

    # 用户权限的获取
    # 回头要查查这个是怎么获取的
    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions
        return all_permissions

    def has_permissions(self, permission):
        return self.permissions & permission == permission

    @property
    def is_super_admin(self):
        return self.has_permissions(CMSPermission.ALL_PERMISSION)

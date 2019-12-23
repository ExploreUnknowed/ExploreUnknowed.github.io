#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"

from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from app import app
from exts import db
from apps.cms.modles import CmsUser, CMSPermission, CMSRole
from apps.front.models import FrontUser
from apps.modles import BoardModel,PostModel,CommentModel,HighlightPostModel

manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)

# 添加后台用户
@manage.option('-u', '--username', dest='username')
@manage.option('-p', '--password', dest='password')
@manage.option('-e', '--email', dest='email')
def create_cms_admin(username, password, email):
    user = CmsUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()

    # 获取用户
    # 添加用户到相应的组里面
@manage.option('-e', '--email', dest='email')
@manage.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    user = CmsUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.user.append(user)
            db.session.commit()
            print('用户添加成功')
        else:
            print('没有这个角色%s' % role)
    else:
        print("没有这个邮箱%s" % email)

# 添加前台用户
@manage.option('-t', '--telephone'  , dest ='telephone')
@manage.option('-u', '--username'  , dest = 'username')
@manage.option('-p', '--password'  , dest = 'password')
def create_front_user(telephone , username ,password):
    user = FrontUser(telephone = telephone ,username = username ,password = password)
    db.session.add(user)
    db.session.commit()

#添加用户权限
@manage.command
def create_role():
    # 访问者
    victor = CMSRole(name='访问者', desc='只能相关数据,不能修改')
    # victor的权限设置
    victor.permissions = CMSPermission.VICTIOR

    # 运营角色
    operator = CMSRole(name='网站运营', desc='基本上就具有全部功能了, 就差一点点')
    operator.permissions = CMSPermission.VICTIOR | CMSPermission.BOARDER | CMSPermission.COMMENTER | CMSPermission.COMUSER | CMSPermission.FRONTUSER | CMSPermission.POSTER

    # 超级管理员账户
    super_admin = CMSRole(name='超级管理员', desc="超级管理员 ,这个权限最大的账户")
    # 超级管理员当然是最大账户的了
    super_admin.permissions = CMSPermission.ALL_PERMISSION
    # add_all 才是以列表的方式添加所有账户
    db.session.add_all([victor, operator, super_admin])
    db.session.commit()


@manage.command
def test_permission():
    # 查找其用法
    user = CmsUser.query.first()
    if user.has_permissions(CMSPermission.VICTIOR):
        print("这个用户有访问者的权限")
    else:
        print("这个用户没有访问者的权限")


if __name__ == '__main__':
    manage.run()

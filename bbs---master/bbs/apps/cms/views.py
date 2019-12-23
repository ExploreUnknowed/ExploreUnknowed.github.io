#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"
from flask import Blueprint, render_template, views, request, session, redirect, url_for, g, jsonify
from .forms import LoginForm, ResetForm, ResetEmailForm, AddBoardForm, UpdateBoardForm
from .modles import CmsUser, CMSPermission
from .decorate import login_required, permission_required
from utils import restful, zlcache
from exts import mail
from flask_mail import Message
from exts import db
from apps.modles import BoardModel, HighlightPostModel, PostModel
import config
import string, random
from tasks import send_mail

# todo 这个以后要做到发送邮箱需要记录在日志里，方便查看，要记录下来给哪些人发送了新的邮件。
# todo  在进行flask分页的时候 还是使用现成的flask-page...，跟bootstrap结合出来的

# todo 记录访问系统的日志，访问bbs论坛的哪个地方，ip是多少，时间是多少，这样才能够更好的维护和安全

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return "cms index"


# 个人中心页面
@bp.route('/probfile/')
@login_required
def probfile():
    return render_template('cms/cms_probfile.html')


# 添加加精帖子视图函数
@bp.route('/hpost/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def hpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('请传入帖子id！')

    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('没有这篇帖子！')

    highlight = HighlightPostModel()
    highlight.post = post

    db.session.add(highlight)
    db.session.commit()
    return restful.success()


# 取消加精帖子视图函数
@bp.route('/uhpost/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def uhpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('请传入帖子id！')

    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('没有这篇帖子！')

    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


# 移除加精帖子视图函数
@bp.route('/dpost/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def dpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('请传入帖子id！')

    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('没有这篇帖子！')

    db.session.delete(post)
    db.session.commit()
    return restful.success()


# 帖子管理模块视图
@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    post_list = PostModel.query.all()
    return render_template('cms/cms_posts.html', posts=post_list)


# 发送邮箱验证码接口
@bp.route('/send_mail/')
def sendmail_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请传递邮箱参数！')
    captcha = list(string.ascii_letters)
    # 获得a-zA-Z的字符串 列表
    captcha_num = map(lambda x: str(x), range(0, 10))
    # 获得0-9的数字 的列表
    captcha.extend(captcha_num)
    # 列表的一个方法，使得列表之间能够继承
    # print("".join(captcha))
    # 结合完毕，剩下就是随机打印出6个不同的字符串和数字了
    result_captcha = random.sample(captcha, 6)
    result_captcha = "".join(result_captcha)
    print(result_captcha)
    message = Message("bbs论坛验证码", recipients=[email],
                      body="关于您更改默认邮箱，我们向您发送了一条邮箱验证码，邮箱验证码为%s ，如果不是本人操作，请自觉忽略" % result_captcha)
    try:
        send_mail.delay('知了论坛邮箱验证码', recipients=[email], body='你的验证码是：%s' % captcha)
    except:
        return restful.server_error()

    zlcache.set(email, captcha)  # 添加验证码缓存
    return restful.success()


# 注销页面
@bp.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect(url_for('cms.login'))


# 评论管理
@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


# 板块管理
@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    board_models = BoardModel.query.all()
    context = {
        'boards': board_models
    }
    return render_template('cms/cms_boards.html', **context)


# 添加板块视图
@bp.route('/aboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data

        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


# 更新板块视图，就是编辑的地方
@bp.route('/uboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块！')
    else:
        return restful.params_error(message=form.get_error())


# 删除板块视图
@bp.route('/dboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error('请输入板块id!')

    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message='没有这个板块！')

    db.session.delete(board)
    db.session.commit()
    return restful.success()


# 前台用户管理
@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')


# cms用户管理
@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.COMUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


# cms组管理
@bp.route('/groles/')
@login_required
@permission_required(CMSPermission.COMUSER)
def groles():
    return render_template('cms/cms_groles.html')


# 登录类视图
class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_layui_login.html', message=message)

    # message在获取之后，再次调用message方法，如果重新渲染的没有message的值，那么传入message的值也没用了

    def post(self):
        form = LoginForm(request.form)
        print(form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.email.data
            user = CmsUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                session.permanent = True
                # 这个加入session之后就是正好31天，一个月
                return redirect(url_for('cms.probfile'))
            else:
                return self.get(message='用户名或者密码错误')
        else:
            print(form.errors)
            self.get(message='表单验证错误')
        return self.get(message='用户名或者密码错误')


# 修改密码功能
class ResetView(views.MethodView):
    decorators = [login_required, permission_required(CMSPermission.VICTIOR)]  # 保证用户登陆

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetForm(request.form)  # 验证修改密码
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user  # 使用g对象传递用户对象
            if user.check_password(oldpwd):
                # 更新数据库中的密码
                user.password = newpwd
                db.session.commit()
                # 返回json数据
                # return jsonify({"code": 200, "message": ""})
                return restful.success()
            else:
                # return jsonify({"code": 400, "message": "旧密码输入错误"})
                return restful.params_error("旧密码错误")
        else:
            message = form.get_error()  # 使用父类的get_error()方法获取错误信息
            # return jsonify({"code": 400, "message": message})
            return restful.params_error(message)


# 修改邮箱
class ResetEmailView(views.MethodView):
    decorators = [login_required, permission_required(CMSPermission.VICTIOR)]

    # 装饰器都是要加decorators的，不加s会报错
    def get(self):
        return render_template('cms/cms_resetmail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            user = g.cms_user
            # 要先从g.cms_user中获取到user 才能够进行修改的
            user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetView.as_view('resetpwd'))

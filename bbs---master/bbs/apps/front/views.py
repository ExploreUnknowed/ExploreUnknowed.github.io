#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"
from flask import Blueprint, views, render_template, make_response, request, session, url_for, g, abort
from utils.captcha import Captcha
from utils import zlcache, restful, safeutils
from io import BytesIO
from .forms import SignupForm, SigninForm, AddPostForm,AddCommentForm
from .models import FrontUser
from exts import db
from .decorate import login_required
import config
from flask_paginate import Pagination, get_page_parameter
from apps.modles import BoardModel, PostModel,CommentModel,HighlightPostModel
from sqlalchemy.sql import  func

bp = Blueprint('front', __name__)


#todo  学习celery 异步机制
#todo  celery的异步机制 celery-A tasks.celery --pool=eventlet worker --loglevel=info 这样就可以执行了

# bbs论坛前台页面，找个页面还是挺不错的，可以学习到很多的东西，不过这个和我之前做的差不太多吧
# todo 帖子管理，用户登录
@bp.route('/')
def index():
    board_id = request.args.get('bd', type=int, default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    sort = request.args.get('st', type=int, default=1)  # 排序因子
    # banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)  # 降序
    boards = BoardModel.query.all()  # 板块
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    if sort == 1:
        #     # 默认按照创建时间倒序排列
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        # 按照加精时间倒序排列
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(
            HighlightPostModel.create_time.desc(), PostModel.create_time.desc())
    elif sort == 3:
        # 按照点赞数量倒序排序 由于还没有添加点赞功能，暂时按照默认排序
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        # 按照评论数量倒序排列
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())

    if board_id:  # 特定板块的帖子
        query_obj = query_obj.filter(PostModel.board_id == board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:  # 全部帖子
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0,
                            inner_window=2)  # 分页器
    context = {  # 上下文
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort,
    }
    return render_template('front/front_index.html', **context)


# 帖子详情视图函数
@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template('front/front_pdetail.html', post=post)

# 添加评论视图函数
@bp.route('/acomment/', methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这篇帖子！')
    else:
        return restful.params_error(form.get_error())


# 验证码视图函数，这个函数要进行保存图片，其中的验证码是根据4位数字，生成一个验证码的图片，注意是一个图片，这个图片比较特殊，我们可以用其他的来解决
@bp.route('/captcha/')
def graph_captcha():
    captcha, image = Captcha.gene_graph_captcha()
    print('图形验证码是：', captcha)  # 打印出图形验证码
    zlcache.set(captcha.lower(), captcha.lower())  # 把验证码添加到memcached缓存中
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


# 添加帖子视图
@bp.route('/apost/', methods=['GET', 'POST'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html', boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data

            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message='没有这个板块！')

            post = PostModel(title=title, content=content)
            post.board = board
            post.author = g.front_user  # 传递前台用户
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


# 写一个前端真的是费劲啊，我真是希望有个好的前端。
class SignupView(views.MethodView):
    def get(self):
        # 跳转到之前的页面,如果存在的话
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        # 验证表单
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data

            # 创建新的前台用户
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            print(form.get_error())  # 打印出错误信息
            return restful.params_error(message=form.get_error())


# 前台登录类视图
class SigninView(views.MethodView):
    def get(self):
        # 跳转到之前的页面，如果有的话
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for('front.signup') and safeutils.is_safe_url(
                return_to):
            return render_template('front/front_signin.html', return_to=return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        # 验证登录
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data

            user = FrontUser.query.filter_by(telephone=telephone).first()
            print(password)
            print(user.check_password(password))
            print(user)
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='手机号码或密码错误！')
        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))

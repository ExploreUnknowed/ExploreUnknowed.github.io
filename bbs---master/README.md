# bbs-
一个小型的bbs论坛开发


安装之前请先删除venv这个虚拟环境，并且保证在自己电脑上有python3的环境。下一步直接安装 pip install -r requirements.txt


# 后端开发
&nbsp;&nbsp;&nbsp;&nbsp;在写后端的时候，我把整个项目基本上分装到了apps的包下面。把后台，公众，前台，ue编辑器分别分成了 cms ,common ,front,ueditor。这个分开的时候，后台就是在cms中，common存储的都是些验证码。front 就是展示用户看的。ueditor 这个是别人分装好的一个Ueditor编辑器。apps.forms.py  这个文件是对form的错误进行筛选，筛选出第一处错误，后面就可以直接是引用BaseForm这个表单了。在apps.modles中存放了一些模型，如前台评论数据表，前台帖子数据表，加精帖子数据表，板块的数据表

# 前端开发
&nbsp;&nbsp;&nbsp;&nbsp;我，刚才写了一大推的东西，不小心一点，然后没保存我.......记录下。。。。
前端使用的框架有两个，bootstrap 和 layui ，其中前台采用的是bootstrap 后台cms 采用的layui 框架。我将全部的html都保存到了templates中了，将css js jqery ajax 全部封装到了static里面了。utils 这个是工具的拓展，里面存放着各种的小脚本。

## 介绍后台开发
&nbsp;&nbsp;&nbsp;&nbsp;cms中先开发的是登录和注册，然后为了防止一些人恶意的攻击我的服务器，遂采用form表单的形式来完成这个。
&nbsp;&nbsp;&nbsp;&nbsp;登录类LoginView，继承了views.Methods
&nbsp;&nbsp;&nbsp;&nbsp;定义了两种请求，分别是get 和 post
&nbsp;&nbsp;&nbsp;&nbsp;+ get 直接是渲染一个'cms/cms_layui_login.html'
&nbsp;&nbsp;&nbsp;&nbsp;+ post方法是先对传入的值进行验证(采用LoginForm)，在LoginForm中先继承了BaseForm这个表单类，然后从前端获取数据的时候，这个命名一定要与前端的name或者jquery里面的值保持一致。对 
&nbsp;&nbsp;&nbsp;&nbsp;   + email-->登录邮箱参数保证必须是string类型所以必须是StringField，然后验证器是正确的email地址，这个地址是经过Email的正则判断，然后设置为必须输入
&nbsp;&nbsp;&nbsp;&nbsp;   + password-->登录密码  因为密码是多样的，所以类型就设置为了StringField，然后在进行验证器的时候，只要保证这个必须要输入就可以了。
&nbsp;&nbsp;&nbsp;&nbsp;   + remember --> 记住密码 这个功能，因为从前端定义了是数字进行传入，所以参数类型就是InterField ，其他的倒没有什么要求
&nbsp;&nbsp;&nbsp;&nbsp;post 方法中用form.validata()是个判定方法
   + 如果符合：读取email password remember的数值，然后从CmsUser中的账号进行对比，如果校对成功就加入到session里面，如果校对失败，就return 一个错误的信息


## 修改密码
&nbsp;&nbsp;&nbsp;&nbsp;还是先读取一个session，然后才能是修改密码，这里要注意是从session里面进行读取的，而不是直接从数据库里面进行判定的，如果直接判定很可能产生越权漏洞(一个用户可以修改多个账号的密码，源于没有加session，并且只对用户进行判定没有对账号和密码进行判定)

## 修改邮箱
&nbsp;&nbsp;&nbsp;&nbsp;修改邮箱和修改密码功能大致类似。

```
 class ResetEmailView(views.MethodView):
    decorators = [login_required, permission_required(CMSPermission.VICTIOR)]

    #装饰器都是要加decorators的，不加会报错
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
```        

&nbsp;&nbsp;&nbsp;&nbsp;这个地方主要是发送一封邮箱，旧的邮箱是不能修改的。先发送一封邮箱，如果是正确的就进行修改邮箱，如果是错误的就不进行修改了。修改邮箱是专用一个接口，即send_email 这个视图，这个是通过ajax的方式发送给后端的。ps：在类视图中，添加装饰器不是通过@的方式，而是通过decorates这样的方式，decorates这个是装饰器的py名称。

## 注销登录

&nbsp;&nbsp;&nbsp;&nbsp;注销登录的前提必须是用户已经登录过了，然后才能注销登录。注销登录其实就是删除一个session，清除session使用session.clear()，全部清除的方式。

## 用户权限管理

&nbsp;&nbsp;&nbsp;&nbsp;权限管理是通过二进制的方式来进行的，二进制的 | ，这个会导致权限的增加。事先设置好几个权限，然后权限用 | 进行叠加。添加权限的方式是通过manage.py中的文件add_user_role 这个函数进行完成的

## 数据库的更新

&nbsp;&nbsp;&nbsp;&nbsp;如果一个表中没有设置好外键而更新有外键的话，可能是会有问题的。更新通过flask manage.py db init flask manage.py db upgrade 这样的命令来进行更新。

## 防御措施

### csrf防御

&nbsp;&nbsp;&nbsp;&nbsp;通过ajax里面有一个通过meta标签中发送一个csrf_token的方式来防御。首先在<meta>标签中有一个name = csrf_token ,然后从前台发送到后台的时候是通过ajax的方式来进行发送了。

### xss 防御

&nbsp;&nbsp;&nbsp;&nbsp;我在信任的html里面加入了safe，这个是jinjia2进行防御xss的一个措施

### sql注入防御

&nbsp;&nbsp;&nbsp;&nbsp;通过sqlalchemy来进行防御的，sqlalchchemy可以防御一些非法字符，如' ] \ 一类的


### ssti 注入防御

&nbsp;&nbsp;&nbsp;&nbsp;ssti注入产生的原因是一个return template.string 这样类似的方式来的，如果采用正好的return templates这样的就是可以避免的


# 重点分析
&nbsp;&nbsp;&nbsp;&nbsp;上传文件都是通过ue编辑器这个编辑器

&nbsp;&nbsp;&nbsp;&nbsp;发送邮箱异步 都是通过celery 和 evenlet这个插件 这些都是包

&nbsp;&nbsp;&nbsp;&nbsp;后台可以对模块进行添加 这个利用的是ajax的异步发送机制，这个机制是通过ajax发送到后端，不是直接从name里面获取

# 注册蓝图

注册蓝图的时候要注意，注册的路由必须和蓝图保持一致

## restful接口

&nbsp;&nbsp;&nbsp;&nbsp;这个接口是根据传入回来的状态码进行判断的，如果传入的是200，会是怎么怎么样，这个也是根据ajax来进行判断的

##  在captcha里面封装的是验证码

&nbsp;&nbsp;&nbsp;&nbsp;验证码写的时候，别人是给我分装好了，我不需要再手动的进行画布，噪点进行编辑了

## manage.py 
&nbsp;&nbsp;&nbsp;&nbsp;里面管理的都是一些用需要用命令行添加的角色，还有创建一些东西

## redis
&nbsp;&nbsp;&nbsp;&nbsp;用redis的时候，我把短信验证码都写道redis里面了，这样可以加快速度，有空还是要多写写redis的方法，redis对于缓存还是比较重要的

## memche

&nbsp;&nbsp;&nbsp;&nbsp;将验证码发送到memache

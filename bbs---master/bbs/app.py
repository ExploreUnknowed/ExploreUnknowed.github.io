from flask import Flask
from apps.cms.views import  bp as cms_bp
from apps.common.views import  bp as common_bp
from apps.front.views import  bp as front_bp
from apps.ueditor import bp as ueditor_bp
from exts import  db,mail,alidayu
from flask_wtf import  CSRFProtect
import  config

app = Flask(__name__)
app.config.from_object(config)
CSRFProtect(app)
# flask在执行config文件的时候，是有顺序的，不是说没有顺序。可能是我之前没有意识到
app.register_blueprint(cms_bp)
app.register_blueprint(common_bp)
app.register_blueprint(front_bp)
app.register_blueprint(ueditor_bp)
db.init_app(app)
mail.init_app(app)
alidayu.init_app(app)
# @app.route('/')
# def hello_world():
#     return 'Hello World!'

# 权限分配的时候一个是前端看不见，一个是后端没有这个权限，这个权限的时候是需要加个装饰器的


if __name__ == '__main__':
    app.run(port=9000 , debug=True)

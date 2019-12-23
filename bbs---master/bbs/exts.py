#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from utils.alidayu import  AlidayuAPI

db = SQLAlchemy()
mail = Mail()
alidayu = AlidayuAPI()





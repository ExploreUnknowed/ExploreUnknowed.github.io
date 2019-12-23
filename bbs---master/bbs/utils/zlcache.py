#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author  : "你们的饭不好吃"

#这个写的是memcache ，将验证码存放到memcache中，这样可以是对验证码的时效加以限制
import  memcache

cache = memcache.Client(['127.0.0.1:11211'] ,debug=True)

#定义set方法 ，用memcache连接并 建立起一个值
def set(key, value, timeout=0):
    return cache.set(key, value, timeout)


def get(key):
    return cache.get(key)


def delete(key):
    return cache.delete(key)

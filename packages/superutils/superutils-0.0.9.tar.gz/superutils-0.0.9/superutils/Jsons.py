#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com


import json



@staticmethod
def createClass(cls):
    class JSONObject(cls):
        def __init__(self, d):
            self.__dict__ = d
    return JSONObject

@staticmethod
def toJson(obj):
    return json.dumps(obj, default=lambda obj: obj.__dict__)


@staticmethod
def toObject(data, obj):
    return json.loads(data,object_hook=createClass(obj.__module__))

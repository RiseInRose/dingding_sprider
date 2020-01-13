#!/usr/bin/env python
# coding=utf-8
# author:uncleyiba@qq.com
# datetime:2020/1/10 下午5:15
import os, sys, re, json, traceback, time
from selenium import webdriver
from flask import Flask, make_response, send_file
from flask_restful import Resource, Api
from sprider import SpriderThread
"""
网页版钉钉入口
https://im.dingtalk.com/
毫无疑问我们首先要起一个webdriver定时去爬取钉钉上的组织架构信息
将其保存下来存在数据库中

我们还需要其一个flask用于访问存储好的结构方便进行展示
展示得包括
1.登录码的访问
2.差异比较页面


"""
app = Flask(__name__, template_folder="template/")
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
api = Api(app)
@api.representation("text/html")
def out_html(data,code, headers=None):
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp


# 首页
@app.route('/', methods=['GET'])
def index():
    return "欢迎访问"

@app.route('/file/<path:path>', methods=['GET'])
def md_file(path):
    print(path)
    return send_file('files\\{0}'.format(path))

@app.route('/static2', methods=['GET'])
def md_file2():
    # print(path)
    # return send_file('files/{0}'.format(path))
    return ""



if __name__ == "__main__":
    sh = SpriderThread("dahua")
    sh.start()


    app.config['JSON_AS_ASCII'] = False
    app.run(port=9999, host="0.0.0.0")



#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2020/1/10 下午5:16
import os, sys, re, json, traceback, time
from selenium import webdriver
from conf.conf import DINGDING_URL


def wait_until_show(show_func, show_func_args, false_func, max_times):
    pass


class Sprider(object):
    def __init__(self, name):
        """

        :param name: 用于区分多个的时候的名字，同样也用于关键显示的地方
        """
        self.name = name


    def run(self):
        driver = webdriver.Chrome()
        driver.get(DINGDING_URL)






if __name__ == "__main__":
    pass

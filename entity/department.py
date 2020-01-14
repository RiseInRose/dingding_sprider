#!/usr/bin/env python
# coding=utf-8
# author:uncleyiba@qq.com
# datetime:2020/1/10 下午5:24
import os, sys, re, json, traceback, time

class Department(object):
    def __init__(self, name):
        self.name = name
        self.member_list = []
        self.child_dept = []
        self.father_dept = None

    def get_data_json(self):
        child_dept = []
        for each_child_dept in self.child_dept:
            child_dept.append(each_child_dept.get_data_json())
        data_json = dict(
            name=self.name,
            child_dept=child_dept,
            member_list=self.member_list
        )
        return data_json


if __name__ == "__main__":
    pass

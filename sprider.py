#!/usr/bin/env python
# coding=utf-8
# author:uncleyiba@qq.com
# datetime:2020/1/10 下午5:16
import os, sys, re, json, traceback, time, datetime, threading, copy
from selenium import webdriver
from conf.conf import DINGDING_URL, RUN_HOUR_NUM
from entity.department import Department
from entity.staff import Staff


def wait_until_show(show_func, show_func_args, false_func, max_times):
    pass


class SpriderThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        sprider = Sprider(self.name)
        sprider.run()


class Sprider(object):
    def __init__(self, name):
        """

        :param name: 用于区分多个的时候的名字，同样也用于关键显示的地方
        """
        self.name = name
        self.driver = webdriver.Chrome()

    def login(self):
        # 登陆二维码的过期时间是三分钟，这里我们设置一分钟的截图
        qrcodes = self.driver.find_elements_by_class_name("qrcode-wrapper")
        # 未登陆  二维码尚存在  则刷新并截图
        if len(qrcodes) > 0:
            self.driver.get(DINGDING_URL)
            qrcode = self.driver.find_element_by_class_name("qrcode-wrapper")
            qrcode.screenshot("files/qrcode.png")
            print("二维码已截图")
            return False
        else:
            print("登陆成功")
            return True


    def run(self):
        while True:
            hour = datetime.datetime.now().hour
            print("当前小时数:{0}".format(hour))
            if hour % RUN_HOUR_NUM == 0:
                data = self.get_data()
                time.sleep(2 * 60 * 60)
            else:
                time.sleep(5 * 60)

    @staticmethod
    def find_children(driver, index_list, father_dept):
        """

        :param driver:
        :param dept_list:  深度   部门名称列表
        :param index_list:  深度   对应的列表的第几个
        :param father_dept:  父部门
        :return:
        """
        time.sleep(2)
        print("{0}{1}{2}".format("  " * len(index_list), father_dept.name, ":"))
        # 进入对应的部门
        driver.find_element_by_class_name("dept-name").click()
        time.sleep(1)
        for each_index in index_list:
            team_items = driver.find_elements_by_class_name("team-item")
            team_items[each_index].click()
            time.sleep(1)


        team_items = driver.find_elements_by_class_name("team-item")
        if len(team_items)==0:
            member_items = driver.find_elements_by_class_name("member-item")
            if len(member_items) > 0:
                member_name_list = []
                for each_member in member_items:
                    member_name = each_member.find_element_by_class_name("avatar").find_element_by_tag_name("div").get_attribute("name")
                    member_name_list.append(member_name)
                print("{0}{1}".format("  " * (len(index_list) + 1), ",".join(member_name_list)))
            else:
                pass
        else:
            for index, each_team in enumerate(team_items):
                dept_name = each_team.find_element_by_class_name("info").text
                dept = Department(dept_name)
                father_dept.child_dept.append(dept)
            for index, each_team in enumerate(team_items):
                new_index_list = copy.deepcopy(index_list)
                new_index_list.append(index)
                Sprider.find_children(driver, new_index_list, father_dept.child_dept[index])





    def get_data(self):
        self.driver.get(DINGDING_URL)
        # 处于未登陆状态则每隔1min刷新一下登陆码
        while not self.login():
            time.sleep(2 * 15)
        # 登陆成功
        self.driver.save_screenshot("files/page.png")
        # 去掉最开始的框
        time.sleep(1)
        try:
            self.driver.find_element_by_class_name("foot").find_element_by_tag_name("button").click()
            print("弹窗已去除")
        except:
            print("未发现弹窗")
            pass
        # 进入组织架构页面
        self.driver.find_element_by_class_name("menu-contact").click()
        # self.driver.find_element_by_class_name("dept-name").click()
        dept_company = Department(self.name)
        self.find_children(self.driver, [], dept_company)









        time.sleep(10)
        self.driver.close()







if __name__ == "__main__":
    sprider = Sprider("daguan")
    sprider.run()


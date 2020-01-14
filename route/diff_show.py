#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-01-14 15:58
import os, sys, re, json, traceback, time
import _locale
from entity.staff import Staff

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])






def get_json_depth(data_json):
    depth = 1
    child_dept_list = data_json["child_dept"]
    if len(child_dept_list) > 0:
        for each in child_dept_list:
            json_depth = get_json_depth(each)
            each["depth"] = json_depth
            if json_depth + 1 > depth:
                depth = json_depth + 1
    else:
        depth = 1
    return depth

def get_depth_member_num(data_json):
    child_dept_list = data_json["child_dept"]
    if len(child_dept_list) ==0:
        data_json["num"] = len(data_json["member_list"])
        return len(data_json["member_list"])
    else:
        num = 0
        for each in child_dept_list:
            num += get_depth_member_num(each)
        data_json["num"] = num
        return num

def get_staff_list(data_json):
    staff_detail_list = []
    staff_list = data_json["member_list"]
    if len(staff_list) == 0:
        child_dept_list = data_json["child_dept"]
        for each in child_dept_list:
            each_staff_list = get_staff_list(each)
            for each_staff in each_staff_list:
                each_staff.dept_list.insert(0, {"name":data_json["name"], "num":data_json["num"]})
            staff_detail_list += each_staff_list
    else:
        for each_staff in staff_list:
            staff = Staff(each_staff)
            staff.dept = data_json["name"]
            staff.dept_list = [{"name":staff.dept, "num":data_json["num"]}]
            staff_detail_list.append(staff)
    return staff_detail_list



def get_dept_table_html(json_data):
    # 得到总深度   +1 为员工列表
    total_depth = get_json_depth(json_data)
    print("组织架构最多为:{0}层".format(total_depth))
    # 人数数据插入
    get_depth_member_num(json_data)
    # 得到员工列表
    staff_list = get_staff_list(json_data)
    # 先整理成表格形式
    table_result = []
    for each_staff in staff_list:
        for i in range(len(each_staff.dept_list), total_depth):
            each_staff.dept_list.append(each_staff.dept_list[-1])
        dept_list = [each["name"] for each in each_staff.dept_list]
        dept_list.append(each_staff.name)
        table_result.append(dept_list)
    # 计算成html
    table_flag = [[False for j in range(total_depth + 1)] for i in range(len(table_result))]
    table_show_result = []
    # print(table_show_result)
    for i, line in enumerate(table_result):
        each_line = []
        for j, cell in enumerate(line):
            if table_flag[i][j]:
                continue
            value = table_result[i][j]
            i_max = i + 1
            j_max = j + 1
            while j_max < len(line):
                cell_value = table_result[i][j_max]
                if value == cell_value:
                    j_max += 1
                else:
                    break
            while i_max< len(table_result):
                cell_value = table_result[i_max][j]
                if value == cell_value:
                    i_max += 1
                else:
                    break
            for a in range(i, i_max):
                for b in range(j, j_max):
                    table_flag[a][b] = True
            each_line.append([value, i_max-i, j_max-j])
        table_show_result.append(each_line)
    show_html = ""
    for each_line in table_show_result:
        show_html += "<tr>"
        for each_cell in each_line:
            show_html += "<td rowspan='{1}' colspan='{2}'>{0}</td>".format(each_cell[0], each_cell[1],each_cell[2])
        show_html += "</tr>"
    print(show_html)









    return table_result






if __name__ == "__main__":
    f = open("../test/data_json1.json", "r")
    data = json.loads(f.read())
    f.close()

    # depth = get_json_depth(data)
    # print(get_depth_member_num(data))
    #
    staff_list = get_dept_table_html(data)
    # # depth = get_json_depth(data)
    # # print(depth)
    for each in staff_list:
        print(each)
        # print("{0}:{1}".format(each.name, each.dept_list))
    # print(staff_list)
    # print(json.dumps(staff_list, ensure_ascii=False, indent=2))
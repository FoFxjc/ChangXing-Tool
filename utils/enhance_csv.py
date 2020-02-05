#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

from utils import basic
from utils import file as file


def load(path, encoding=None):
    """ 加载csv文件
    :param path: <str> 文件所在路径
    :param encoding: <str> 文件编码格式
    :return: <_csv.reader> csv格式的文件内容
    """
    try:
        csv_file = open(path, mode="r", encoding=encoding)
        return csv.reader(csv_file)
    except FileNotFoundError:
        print("未找到文件:" + path)


def find_column(title_list, aim_title):
    """ 在csv文件的标题行中找到目标列名对应的列坐标
    :param title_list: <list> csv的标题行
    :param aim_title: <str> 需要检索列坐标的列名
    :return: <int/None> 目标列名对应的列坐标(若列名不存在则返回None)
    """
    for j in range(0, len(title_list)):
        if title_list[j] == aim_title:
            return j
    return None


def find_some_column(title_list, aim_title_list):
    """ 在csv文件的标题行中找到目标列名(多个)对应的列坐标
    :param title_list: <list> csv的标题行
    :param aim_title_list: <list> 需要检索列坐标的列名(多个)列表
    :return: <dict> 目标列名(多个)对应的列坐标字典,例如: {'平台':1, '目前名称':2}
    """
    result = {}
    for aim_title in aim_title_list:
        result[aim_title] = find_column(title_list, aim_title)
    return result


def get_value(line, column_name, cn_list, if_none=None):
    """ 读取csv某行数据中固定列的值
    :param line: <list> 需要读取数据的行数据
    :param column_name: <str> 需要读取数据的列名
    :param cn_list: <dict> 列名对应的列坐标字典,形如find_some_column的返回结果,例如: {'平台':1, '目前名称':2}
    :param if_none: <object> 如果列坐标字典不包含该列,或csv中不存在该列,返回的返回值
    :return: <object/None> csv某行数据中某列的值,或设定的为空返回值
    """
    if column_name not in cn_list:
        return if_none
    if cn_list[column_name] is None:
        return if_none
    return line[cn_list[column_name]]


def some_value_is_none(line, column_name_dict):
    """ 判断一行的中部分列是否存在空值
    :param line: <list> 需要判断是否为空值的行数据
    :param column_name_dict: <dict> 需要判断的列名对应的列坐标字典,形如find_some_column的返回结果,例如: {'平台':1, '目前名称':2}
    :return: <bool> 返回是否存在值为空的单元格:True=是,False=否
    """
    if column_name_dict is None:
        return False
    for i in column_name_dict:
        if line[column_name_dict[i]] == "":
            return True
    return False


def get_some_value(line, column_name_list, column_name_dict, if_none=None):
    """ 批量读取一行数据中的部分列,并选择返回list或该数据内容
    :param line: <list> 需要读取数据的行数据
    :param column_name_list: <list> 需要读取的列名列表
    :param column_name_dict: <dict> 列名对应的列坐标字典,形如find_some_column的返回结果,例如: {'平台':1, '目前名称':2}
    :param if_none: <object> 如果列坐标字典不包含该列,或csv中不存在该列,返回的返回值
    :return:
    若读取超过一列,则结果按col_n_list中的顺序,返回:[数据,数据,...]
    若读取一列,返回: <object> 该单元格的内容
    """
    if len(column_name_list) > 1:
        row_value = []
        for item in column_name_list:
            row_value.append(get_value(line, item, column_name_dict, if_none=if_none))
        return row_value
    else:
        return get_value(line, column_name_list[0], column_name_dict, if_none=if_none)


def get_data(path, classify_column_name, column_name, encoding=None, console=False,
             classify_unique=False, not_none_column_name=None):
    """ 批量读取整个csv表格每行中部分列的数据,并依据其中的某些列(大于等于一列)对数据进行分类
    :param path: <str> csv文件路径地址
    :param classify_column_name: <list> 依据某些列单元格的值对结果汇总,则填写这些列的列名,不能为空
    :param column_name: <list> 需要读取的列的列名列表
    :param encoding: <str> csv文件读取使用的编码格式
    :param console: <bool> 是否将警告输出到控制台
    :param classify_unique: <bool> 每个分类是否只需要唯一值
    :param not_none_column_name: <list> 不允许为空值的列名列表
    :return: <dict> 返回读取Excel表单的结果,按行顺序排序,按col_title_list中的顺序排序
    若每个分类拥有唯一值,且读取多列,以有两层分类为例,返回:
    {"一级分类1":{"二级分类1":[数据,数据],"二级分类2":[数据,数据]},"一级分类2":{"二级分类1":[数据,数据],"二级分类2":[数据,数据]}}
    函数支持有超过两层分类,其中各层分类间的数据结构与以上结构相似,内层数据结构与get_sheet_in_classify的返回结果类似
    """
    result = {}
    if not file.is_exist(path):
        return result
    csv_file = load(path, encoding=encoding)  # 读取csv文件
    title = next(csv_file)  # 读取csv标题行
    csv_len_column = len(title)  # 读取csv标题行列数
    column_name_dict = find_some_column(title, column_name)
    classify_column_name_list = find_some_column(title, classify_column_name)
    not_none_column_name_list = find_some_column(title, not_none_column_name)
    for tLine in csv_file:
        if some_value_is_none(tLine, classify_column_name_list) or some_value_is_none(tLine, not_none_column_name_list):
            if console:
                print("CSV文件读取警告:" + path + ",分类数据或不应为空值的数据为空值")
            continue
        if len(tLine) != csv_len_column:
            if console:
                print(
                    "CSV文件读取警告:" + path + ",记录列数不等于标题列数,csv文件标题列数:" + str(csv_len_column) + ",该行列数:" + str(len(tLine)))
            continue
        data_item = get_some_value(tLine, column_name, column_name_dict)
        classify = result
        for j in range(len(classify_column_name) - 1):
            classify_name = tLine[classify_column_name_list[classify_column_name[j]]]
            if classify_name not in classify:
                classify[classify_name] = {}
            classify = classify[classify_name]
        last_classify_name = tLine[classify_column_name_list[classify_column_name[len(classify_column_name) - 1]]]
        if classify_unique:
            classify[last_classify_name] = data_item
        else:
            basic.add_dict_to_list(result, classify, data_item)
    return result


def get_data_list(path, column_name, encoding=None, console=False, iNn_Column_name=None):
    """ 批量读取整个csv表格每行中部分列的数据
    :param path: <str> csv文件路径地址
    :param column_name: <list> 需要读取的列的列名列表
    :param encoding: <str> csv文件读取使用的编码格式
    :param console: <bool> 是否将警告输出到控制台
    :param iNn_Column_name: <list> 不允许为空值的列名列表
    :return: <list> 返回读取Excel表单的结果,按行顺序排序,按col_title_list中的顺序排序
    若读取超过一列,则结果按col_n_list中的顺序,返回:[[数据,数据],[数据,数据]]
    若读取一列,返回:[数据,数据]
    """
    result = []
    if not file.is_exist(path):
        return result
    csv_file = load(path, encoding=encoding)  # 读取csv文件
    title = next(csv_file)  # 读取csv标题行
    csv_len_column = len(title)  # 读取csv标题行列数
    column_name_dict = find_some_column(title, column_name)
    not_none_column_name_list = find_some_column(title, iNn_Column_name)
    for tLine in csv_file:
        if some_value_is_none(tLine, not_none_column_name_list):
            if console:
                print("CSV文件读取警告:" + path + ",分类数据或不应为空值的数据为空值")
            continue
        if len(tLine) != csv_len_column:
            if console:
                print("CSV文件读取警告:" + path + ",记录列数不等于标题列数,csv文件标题列数:" + str(csv_len_column) + ",该行列数:" + str(len(tLine)))
            continue
        result.append(get_some_value(tLine, column_name, column_name_dict))
    return result

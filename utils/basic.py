#!/usr/bin/env python
# -*- coding: utf-8 -*-


import copy
import sys


def double(obj):
    """ 将目标对象复制为两个对象
    :param obj:需要复制的对象
    :return:完成复制的两个对象
    """
    return copy.deepcopy(obj), copy.deepcopy(obj)


def regex_format(string):
    """ 将字符串转义为正则表达式的字符串
    :param string: <str> 需要转义的字符串
    :return: <str> 转义为正则表大会格式的字符串
    """
    return string.replace(r"$", r"\$").replace(r"(", r"\(").replace(r")", r"\)").replace(r"*", r"\*") \
        .replace(r"+", r"\+").replace(r".", r"\.").replace(r"[", r"\[").replace(r"]", r"\]").replace(r"?", r"\?") \
        .replace(r"\\", r"\\\\").replace(r"^", r"\^").replace(r"{", r"\{").replace(r"}", r"\}").replace(r"|", r"\|")


def is_element_in_list(list1, list2):
    """ 判断当前列表(list1)中是否有元素出现在目标列表(list2)中
    :param list1: <list> 当前列表
    :param list2: <list> 目标列表
    :return: <bool> 有元素出现在目标列表中=True; 没有元素出现在目标列表中=False
    """
    for trait_per_champion in list1:
        if trait_per_champion in list2:
            return True
    return False


def list_len_not_zero(obj: list):
    """ 统计列表中不为0的元素的数量
    :param obj: <list> 需要统计元素数量的列表(不一定要求list内所有数据均为数字)
    :return: <int> 列表中不为0的元素的数量
    """
    num = 0
    for i in obj:
        if isinstance(i, int) or isinstance(i, float):
            if i != 0:
                num += 1
    return num


def avg(obj, not_zero: bool = False):
    """ 计算列表中数据的平均值
    :param obj: <list> 需要计算平均值的列表
    :param not_zero: <int> 是否考虑为0的元素:除以列表元素总数=False(默认),除以列表非0元素数=True
    :return: <float> 列表中数据的平均值
    """
    if not_zero:
        return cnt_divide_not_zero(sum(obj), list_len_not_zero(obj))
    else:
        return cnt_divide_not_zero(sum(obj), len(obj))


def merge(*obj):
    """ 合并多个list
    :param obj: <list> 需要合并的list
    :return: <list> 合并完成的list
    """
    result = []
    for tList in obj:
        result.extend(tList)
    return result


def set_value_in_list(obj, index, value, default=0):
    """ 批量将值写入到List中(若写入内容超出List长度则加长List)
    :param obj: <list> 需要写入数据的List
    :param index: <int> 开始写入数据的List坐标
    :param value: <list> 需要需要写入到List中的数据
    :param default: <object> 若列表长度不足index坐标时，自动补齐填写的值
    :return: <list> 合并完成的list
    """
    if index >= len(obj):
        obj.extend([default for _ in range(index - len(obj))])
    for i in range(len(value)):
        if index + i < len(obj):
            obj[index + i] = value[i]
        else:
            obj.append(value[i])


def get_value_from_dict(obj: dict, *keys, if_none=None):
    """ 多次使用key提取dict中数据,并当key不正确时候不报错而是返回规定的值
    :param obj: <dict> 需要提取数据的dict
    :param keys: <*object> 用来提取dict中数据的key
    :param if_none: <object> 若key不正确时返回的值
    :return: <object> 从dict中提取的数据或规定的返回值
    """
    try:
        now = obj
        for key in keys:
            try:
                now = now[key]
            except TypeError:
                return if_none
        return now
    except KeyError or TypeError:
        return if_none


def filter_dict(obj: dict, catalog):
    """ 根据key筛选dict中的数据,将key不包含于目录列表的数据移除
    :param obj: <dict> 需要筛选数据的dict
    :param catalog: <dict/list> 筛选key使用的目录列表
    :return: <None>
    """
    del_list = []
    for item in obj:
        if item not in catalog:
            del_list.append(item)
    for del_item in del_list:
        del (obj[del_item])


def dict_convert(word, convert_list):
    """ 根据转换规则表转换字符串(改名表)
    :param word: <str> 需要被检查是否需要转换的字符串
    :param convert_list: <dict> 转换规则表
    :return: <str> 转换完成的字符串
    """
    if word in convert_list:
        return convert_list[word]
    else:
        return word


def is_number(obj):
    """ 变量/对象是否为数字类变量
    :param obj: <object> 需要判断类型的变量/对象
    :return: <bool> 是否为数字类变量(True=是,False=否)
    """
    if isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, bool) or isinstance(obj, complex):
        return True
    else:
        return False


def cnt_divide_not_zero(dividend, divisor):
    """ 继续除法运算,若除数为0则不再报错而是返回0
    :param dividend: <float> 被除数
    :param divisor: <float> 除数
    :return: <float> 除法结果
    """
    if float(divisor) == 0:
        return 0
    else:
        return float(dividend) / float(divisor)


def add_dict_to_list(obj, key, value_in_list):
    """ 将值添加到dict的list中(若list不存在则创建空list添加)
    :param obj: <dict> 需要添加值的Dict对象
    :param key: <object> 需要添加值的List在obj中的key
    :param value_in_list: <object> 需要添加的值
    :return: <None>
    """
    if key not in obj:
        obj[key] = []
    obj[key].append(value_in_list)


def not_null_list(param_list):
    """ 返回列表本身,若列表为空则返回空列表
    :param param_list: <list/None> 列表或空值
    :return: <list> 结果列表
    """
    if param_list is not None:
        return param_list
    else:
        return []


def sys_exit(reason, status=1):
    """ 报错结束程序
    :param reason: <str> 报错信息
    :param status: <int> 程序退出状态码
    :return: <None>
    """
    print(reason)
    input("回车结束程序...")
    sys.exit(status)

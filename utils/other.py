#!/usr/bin/env python
# -*- coding: utf-8 -*-


def str_2_byte_to_1_byte(string):
    """ 将全角字符转化为半角字符
    :param string: <str> 需要转化为半角的字符串
    :return: <str> 转化完成的字符串
    """
    result = ""
    for uchar in string:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        result += chr(inside_code)
    return result


def str_1_byte_to_2_byte(string):
    """ 将半角字符转化为全角字符
    :param string: <str> 需要转化为全角的字符串
    :return: <str> 转化完成的字符串
    """
    result = ""
    for uchar in string:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif 32 <= inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248

        result += chr(inside_code)
    return result

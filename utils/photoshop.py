# coding=utf-8

"""
图片处理工具包
"""

import math

from PIL import Image


def posterize_code(code, level):
    """ [图像-调整-色调分离]各点的RGB转换算法
    :param code: RGB的值
    :param level: 色阶
    """
    return math.floor(math.floor(code / (256 / level)) * (255 / (level - 1)))


def mixed_mode_partition(code_1, code_2):
    """ [图层-混合模式-划分]各点的RGB转换算法
    :param code_1: 基色点RGB的值
    :param code_2: 混合色点RGB的值
    """
    return math.floor((code_1 / code_2) * 255) if code_2 > 0 else 0


def mixed_mode_difference(code_1, code_2):
    """ [图层-混合模式-差值]各点的RGB转换算法
    :param code_1: 第一个图层RGB的值
    :param code_2: 第二个图层RGB的值
    """
    return abs(code_1 - code_2)


def mixed_mode_multiply(code_1, code_2):
    """ [图层-混合模式-正片叠底]各点的RGB转换算法
    :param code_1: 第一个图层RGB的值
    :param code_2: 第二个图层RGB的值
    """
    return math.floor(code_1 * code_2 / 255)


def color_folded(image, num=100, posterize=None, percent=False, threshold=None):
    """ 汇总统计图片中出现频率最高的颜色
    :param image:(PIL.Image)图片对象
    :param num:(int)输出出现频率最高的颜色数量
    :param posterize:(int/None)是否开启色调分离.None=关闭,int=开启后的色阶数
    :param percent:(bool)输出结果频次/频率选择:True=频率,False=频次
    :param threshold:(int/None)是否按阈值筛选颜色:None=关闭,float=输出要求最低出现频率的阈值
    """
    width, height = image.size  # 读取图片宽高尺寸

    color_dict_temp = {}  # 定义图片颜色频次字典(key=256进制RGB颜色,value=在图片中出现频次)

    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))  # 读取目标点(x,y)的RGB颜色
            if posterize is not None:
                r = posterize_code(r, posterize)
                g = posterize_code(g, posterize)
                b = posterize_code(b, posterize)
            total = r * 65536 + g * 256 + b  # 将颜色编码为256进制RGB颜色
            if total in color_dict_temp.keys():
                color_dict_temp[total] += 1
            else:
                color_dict_temp[total] = 1

    color_list = [(key, val) for key, val in zip(color_dict_temp.keys(), color_dict_temp.values())]  # 将颜色频次字典转化为List
    color_list = sorted(color_list, key=lambda color: color[1], reverse=True)  # 按颜色出现频次排序颜色频次列表
    color_list = color_list[:num]  # 截取出现频次最高的100个颜色

    color_dict = {}  # 定义最终的图片颜色频次字典(key=(r,G,B),value=在图片中出现频次)
    for i in color_list:
        r = math.floor(i[0] / 65536)
        g = math.floor((i[0] % 65536) / 256)
        b = math.floor(i[0] % 256)
        if threshold is None or (i[1] / (width * height)) > threshold:
            if percent:
                color_dict[(r, g, b)] = i[1] / (width * height)
            else:
                color_dict[(r, g, b)] = i[1]

    return color_dict


def color_count(image, *colors, vague=0):
    """ 统计某种颜色的出现频率
    :param image: <PIL.Image> 图片对象
    :param colors: <(int,int,int),...> 需要统计出现频率的颜色RGB值
    :param vague: <int> 颜色模糊程度(RGB各通道允许误差量)
    :return <int> 在图片中目标颜色点的数量
    """
    width, height = image.size  # 读取图片宽高尺寸
    count = [0 for _ in range(0, len(colors))]  # 颜色出现频数
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))  # 读取目标点(x,y)的RGB颜色
            for i in range(len(colors)):
                color = colors[i]
                if abs(color[0] - r) <= vague and abs(color[1] - g) <= vague and abs(color[2] - b) <= vague:
                    count[i] += 1
    return count


def color_first(image, color, vague=0):
    """ 统计某种颜色出现的最靠近左上角的位置坐标
    :param image: <PIL.Image> 图片对象
    :param color: <int,int,int> 需要查找颜色的RGB值
    :param vague: <int> 颜色模糊程度(RGB各通道允许误差量)
    :return <int,int> 目标点的X坐标，目标点的Y坐标
    """
    width, height = image.size  # 读取图片宽高尺寸
    for s in range(width + height - 1):  # 到左上角的数值距离(x+y)从小到大循环
        # 计算x轴最小值
        if s >= height:
            min_x = s - height + 1
        else:
            min_x = 0
        # 从左下向右上循环
        for x in range(min_x, width):
            y = s - x
            if y < 0:
                break
            else:
                r, g, b = image.getpixel((x, y))  # 读取目标点(x,y)的RGB颜色
                if abs(color[0] - r) <= vague and abs(color[1] - g) <= vague and abs(color[2] - b) <= vague:
                    return x + 1, y + 1
    return None


def photo_differ_small(img1, img2, size=12):
    """
    图片相关性比较(通过缩小图比较)
    :param img1:图片1
    :param img2:图片2
    :param size:缩小缩略图像素数
    """
    change1 = img1.resize((size, size))  # 将图1缩小为12px*12px
    change2 = img2.resize((size, size))  # 将图2缩小为12px*12px
    total = 0
    for x in range(size):
        for y in range(size):
            r_1, g_1, b_1 = change1.getpixel((x, y))
            r_2, g_2, b_2 = change2.getpixel((x, y))
            total += (abs(r_1 - r_2) + abs(g_1 - g_2) + abs(b_1 - b_2)) / (255 * 3)
    return total


# 窦式处理法
def dcy_background(picture, background):
    """ 窦式背景剔除法
    要求目标图和背景图的宽高完全相同
    :param picture:(PIL.Image)目标图
    :param background:(PIL.Image)背景图
    :return:(PIL.Image)剔除背景的图
    """
    width, height = picture.size
    if background.size[0] != width or background.size[1] != height:
        return None
    temp_multiply = Image.new("RGB", picture.size, (255, 255, 255))
    temp_partition = Image.new("RGB", picture.size, (255, 255, 255))
    for x in range(width):
        for y in range(height):
            s_r, s_g, s_b = picture.getpixel((x, y))  # 读取目标图对应点RGB
            b_r, b_g, b_b = background.getpixel((x, y))  # 读取背景图对应点RGB
            p_r = mixed_mode_partition(s_r, b_r)  # 图层-混合模式-划分
            p_g = mixed_mode_partition(s_g, b_g)  # 图层-混合模式-划分
            p_b = mixed_mode_partition(s_b, b_b)  # 图层-混合模式-划分
            f_r = mixed_mode_difference(s_r, b_r)  # 图层-混合模式-差值
            f_g = mixed_mode_difference(s_g, b_g)  # 图层-混合模式-差值
            f_b = mixed_mode_difference(s_b, b_b)  # 图层-混合模式-差值
            m_r = mixed_mode_multiply(p_r, f_r)  # 图层-混合模式-正片叠底
            m_g = mixed_mode_multiply(p_g, f_g)  # 图层-混合模式-正片叠底
            m_b = mixed_mode_multiply(p_b, f_b)  # 图层-混合模式-正片叠底
            temp_multiply.putpixel((x, y), (m_r, m_g, m_b))  # 生成正片叠底图层
            temp_partition.putpixel((x, y), (p_r, p_g, p_b))  # 生成划分图层
    return Image.blend(temp_multiply, temp_partition, 0.5)

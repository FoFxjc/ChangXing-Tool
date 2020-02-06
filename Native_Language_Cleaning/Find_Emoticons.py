import re


def find_emoticons(sentence: str):
    """ 在字符串中识别颜文字
    :param sentence: <str> 需要识别的句子
    :return: <list> 识别出的颜文字
    """
    number_list = list("0123456789")  # 数字列表
    common_list = list(",.?!，。、？！T()（）《》")  # 其他常用字符列表
    emoticons_list = list()
    for maybe_emoticons in re.findall("[^a-zA-SU-Z\u4e00-\u9fa5]{2,}", sentence):  # 匹配连续两个以上非文字字符
        character_list = set()
        for character in maybe_emoticons:
            if character not in character_list and character not in number_list and character not in common_list:
                character_list.add(character)
        if len(character_list) <= 1:
            continue
        print("疑似颜文字:", maybe_emoticons)
        emoticons_list.append(maybe_emoticons)
    return emoticons_list


if __name__ == "__main__":
    string = "稳一点啊阿水（/TДT)/"
    print(find_emoticons((string)))

# 运行结果:
#  ['（/TДT)/']

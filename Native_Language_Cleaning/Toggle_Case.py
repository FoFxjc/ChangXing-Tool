if __name__ == "__main__":
    string = "ig加油，Ig冲冲冲"
    print(string.upper())  # 将所有字符中的小写字母转换成大写字母
    print(string.lower())  # 将所有字符中的大写字母转换成小写字母
    print(string.capitalize())  # 若第一个字符为字母，则将其转化为大写字母，其余小写
    print(string.title())  # 将每个单词的第一个字母转化为大写，其余小写

# 运行结果:
# IG加油，IG冲冲冲
# ig加油，ig冲冲冲
# Ig加油，ig冲冲冲
# Ig加油，Ig冲冲冲

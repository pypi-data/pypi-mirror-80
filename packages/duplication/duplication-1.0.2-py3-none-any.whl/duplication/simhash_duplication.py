#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/9/14 18:13
# @Author  : 程婷婷
# @FileName: simhash_duplication.py
# @Software: PyCharm
from simhash import Simhash
import pandas as pd
import time
from zhon.hanzi import punctuation
def simhash_similarity(text1, text2):
    a_simhash = Simhash(text1)
    b_simhash = Simhash(text2)
    # print(a_simhash.value)
    # print(b_simhash.value)
    max_hashbit = max(len(bin(a_simhash.value)), len(bin(b_simhash.value)))
    # print(max_hashbit)
    # 汉明距离
    distince = a_simhash.distance(b_simhash)
    # print(distince)
    similar = 1-distince/max_hashbit
    return similar

def split_line(line):
    table = str.maketrans('','',punctuation)
    # 对行进行分词，去除标点符号，按空白字符分词
    wipe_line = line.translate(table)
    # print(wipe_line)
    return wipe_line



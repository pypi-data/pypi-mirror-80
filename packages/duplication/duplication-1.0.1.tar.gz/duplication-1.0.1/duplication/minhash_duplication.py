#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/9/14 15:37
# @Author  : 程婷婷
# @FileName: minhash_duplication.py
# @Software: PyCharm
from datasketch import MinHash
from zhon.hanzi import punctuation
import jieba
import pandas as pd
import time
# 储存带分词的数据行
Amazon_split = []
a_split = []
b_split = []
# 标点符号的翻译字典

def split_line(line):
    # 对行进行分词，去除标点符号，按空白字符分词
    table = str.maketrans('', '', punctuation)
    wipe_line = line.translate(table)
    split_line = jieba.lcut(wipe_line)
    return split_line
def read_txt(path='a.txt'):
# 读入amazon数据集并分词，以列表保存原数据行和分词结果
    with open(path, encoding='utf-8') as Amazon:
        for line in Amazon.readlines():
            line = line.rstrip('\n')
            Amazon_split.append([line, split_line(line)])

# 定义计算两行文本jaccard相似度的函数
def calculate_jaccard(text1,text2):
    # 计算两行文本的jaccard相似度
    minihash1, minihash2 = MinHash(), MinHash()
    for word in text1:
        minihash1.update(word.encode('utf-8'))
    for word in text2:
        minihash2.update(word.encode('utf-8'))
    return minihash1.jaccard(minihash2)







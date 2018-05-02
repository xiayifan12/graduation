import math
import random

'''
@Author:xiayifan
@Function:提供一些数学工具，如激励函数，随机数，矩阵生成等

'''
random.seed(0)


# 工具函数定义
def rand(a, b):
    return (b - a) * random.random() + a


def make_matrix(m, n, fill=0.0):  # 创造矩阵m x n
    mat = []
    for i in range(m):
        mat.append([fill] * n)
    return mat


def sigmoid(x, con=True):  # 激励函数以及其导函数，con参数为false时为导函数
    if con:
        re = 1.0 / (1.0 + math.exp(-x))
        return re
    else:
        return x * (1 - x)

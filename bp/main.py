import numpy
import random
import math


def rand(a, b):
    return (b - a) * random.random() + a


def make_matrix(m: object, n: object, fill: object = 0.0) -> object:  # 创造矩阵
    mat = []
    for i in range(m):
        mat.append([fill] * n)
    return mat


def sigmoid(x, con):  # 激励函数以及其导函数，con参数为false时为导函数
    if con:
        return 1.0 / (1.0 + math.exp(-x))
    else:
        return x * (1 - x)


class BPNeuralNetwork:
    def __init__(self):
        self.input_n = 0
        self.hidden_n = 0
        self.output_n = 0
        self.input_weight = []
        self.output_weight = []
        self.input_cells = []
        self.hidden_cells = []
        self.output_cells = []
        self.input_correction = []
        self.output_correction = []

    def start(self, ni, nh, no):
        self.input_n = ni + 1  # 输入层加一个偏置神经元
        self.hidden_n = nh  # 隐含层
        self.output_n = no  # 输出层
        # 初始化神经元
        self.input_n = [1.0] * self.input_n
        self.hidden_n = [1.0] * self.hidden_n
        self.output_n = [1.0] * self.output_n
        # 初始化权重（构造邻接矩阵）
        self.input_weight = make_matrix(self.input_n, self.hidden_n)  # 输入层与隐含层之间的权重
        self.output_weight = make_matrix(self.hidden_n, self.output_n)  # 隐含层与输出层之间的权重
        # 随机初始化权重（-0.2到0.2）
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                self.input_weight[i][h] = rand(-0.2, 0.2)
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                self.output_weight[h][o] = rand(-0.2, 0.2)
        # 初始化修正矩阵
        self.input_correction = make_matrix(self.input_n, self.hidden_n)
        self.output_correction = make_matrix(self.hidden_n, self.output_n)

    def predict(self, inputs):  # 完成一次正向传播
        for i in range(self.input_n - 1):
            self.input_cells[i] = inputs[i]
        # 隐含层
        for j in range(self.hidden_n):
            total = 0.0
            for i in range(self.input_n):
                total += self.input_cells[i] * self.input_weight[i][j]
            self.hidden_cells[j] = sigmoid(total, True)
        # 输出层
        for k in range(self.output_n):
            total = 0.0
            for j in range(self.hidden_n):
                total += self.hidden_cells[j] * self.output_weight[j][k]
            self.output_cells[k] = sigmoid(total, True)
        return self.output_cells[:]

    def back_propagate(self, case, label, learn, correct):
        # 完成一次前向传播
        self.predict(case)
        # 计算out误差
        output_deltas = [0.0] * self.output_n
        for o in range(self.output_n):
            error = label[o] - self.output_cells[o]
            output_deltas[o] = sigmoid(self.output_cells[o], False) * error
        # 计算hidden误差
        hidden_deltas = [0.0] * self.hidden_n
        for h in range(self.hidden_n):
            error = 0.0
            for o in range(self.output_n):
                error += output_deltas[o] * self.output_weight[h][o]
            hidden_deltas[h] = sigmoid(self.hidden_cells[h]) * error
        # 更新权重
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                change = output_deltas[o] * self.hidden_cells[h]
                self.output_weight[h][o] += learn * change + correct * self.output_correction[h][o]
                self.output_correction[h][o] = change

        for i in range(self.input_n):
            for h in range(self.hidden_n):
                change = hidden_deltas[h] * self.input_cells[i]
                self.input_weight[i][h] += learn * change + correct * self.input_correction[i][h]
                self.input_correction[i][h] = change
        # 全局损失
        error = 0.0
        for o in range(len(label)):
            error += 0.5 * (label[o] - self.output_cells[o]) ** 2  # 均方误差
        return error

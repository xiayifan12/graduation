from bp.Util.mathTools import rand, make_matrix, sigmoid
from bp.Setting.basesetting import NUM_OF_OUTPUT, NUM_OF_HIDDEN, NUM_OF_INPUT, LEARNING_RATE, CORRECT_RATE, RANGE_UNDER, \
    RANGE_UPDER, FINAL_ERROR, MAX_TIME
from bp.Util.DataHandle import HandleLabel, MaxMinNormalization
from bp.Util.VisualizationTools import showGraphWithIters
from random import shuffle

'''
@Author:xiayifan
@Function:该模块定义了核心的bp神经网路类
@Update : 4/11 改变思路，将回归问题转换为分类问题
'''


# 核心bp神经网络类
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
        self.error_history = []
        self.maxNorm = []
        self.minNorm = []

    def start(self, ni, nh, no):
        self.input_n = ni + 1  # 输入层加一个偏置神经元
        self.hidden_n = nh  # 隐含层
        self.output_n = no  # 输出层
        # 初始化神经元
        self.input_cells = [1.0] * self.input_n
        self.hidden_cells = [1.0] * self.hidden_n
        self.output_cells = [1.0] * self.output_n
        # 初始化权重（构造邻接矩阵）
        self.input_weight = make_matrix(self.input_n, self.hidden_n)  # 输入层与隐含层之间的权重
        self.output_weight = make_matrix(self.hidden_n, self.output_n)  # 隐含层与输出层之间的权重
        # 随机初始化权重
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                self.input_weight[i][h] = rand(RANGE_UNDER, RANGE_UPDER)
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                self.output_weight[h][o] = rand(RANGE_UNDER, RANGE_UPDER)
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
            self.hidden_cells[j] = sigmoid(total)
        # 输出层
        for k in range(self.output_n):
            total = 0.0
            for j in range(self.hidden_n):
                total += self.hidden_cells[j] * self.output_weight[j][k]
            self.output_cells[k] = sigmoid(total)
            # self.output_cells[k] = total
        return self.output_cells[:]

    def back_propagate(self, case, label, learn, correct):
        # 完成一次前向传播
        self.predict(case)
        # 计算out误差
        output_deltas = [0.0] * self.output_n
        for o in range(self.output_n):
            error = label[o] - self.output_cells[o]
            output_deltas[o] = sigmoid(self.output_cells[o], False) * error
            # output_deltas[o] = error
        # 计算hidden误差
        hidden_deltas = [0.0] * self.hidden_n
        for h in range(self.hidden_n):
            error = 0.0
            for o in range(self.output_n):
                error += output_deltas[o] * self.output_weight[h][o]
            hidden_deltas[h] = sigmoid(self.hidden_cells[h], False) * error
        # 更新权重
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                change = output_deltas[o] * self.hidden_cells[h]
                # self.output_weight[h][o] += learn * change
                self.output_weight[h][o] += learn * change + correct * self.output_correction[h][o]
                self.output_correction[h][o] = change

        for i in range(self.input_n):
            for h in range(self.hidden_n):
                change = hidden_deltas[h] * self.input_cells[i]
                # self.input_weight[i][h] += learn * change
                self.input_weight[i][h] += learn * change + correct * self.input_correction[i][h]
                self.input_correction[i][h] = change
        # 全局损失
        error = 0.0
        for o in range(len(label)):
            error += (label[o] - self.output_cells[o]) ** 2  # 均方误差
        return error

    def train(self, casesR, labelsR, limit=1000, learn=0.5, correct=0.1):
        retrunThings = MaxMinNormalization(casesR)
        cases = retrunThings[0]
        labels = HandleLabel(labelsR)
        self.maxNorm = retrunThings[1]
        self.minNorm = retrunThings[2]
        for j in range(limit):
            error = 0.0
            for i in range(len(cases)):
                label = labels[i]
                case = cases[i]
                error += self.back_propagate(case, label, learn, correct)
            error_in_sample = 0.5 * (error / len(cases))
            self.error_history.append(error_in_sample)
            if error <= FINAL_ERROR:
                break

    def test(self, cases, labels):
        self.start(NUM_OF_INPUT, NUM_OF_HIDDEN, NUM_OF_OUTPUT)
        self.train(cases, labels, MAX_TIME, LEARNING_RATE, CORRECT_RATE)

    def forecase(self, delay, shake, packet, bandwidth):
        caseR = [delay, shake, packet, bandwidth]
        case = []
        for i in range(len(caseR)):
            x = (caseR[i] - self.minNorm[i]) / (self.maxNorm[i] - self.minNorm[i])
            case.append(x)
        self.predict(case)
        result = []
        Qoe = ""
        maxvalue = max(self.output_cells)
        for i in self.output_cells:
            if i == maxvalue:
                result.append(1)
            else:
                result.append(0)
        for i in range(5):
            if result[i] == 1:
                if i == 0:
                    Qoe = "很差"
                if i == 1:
                    Qoe = "较差"
                if i == 2:
                    Qoe = "中等"
                if i == 3:
                    Qoe = "较好"
                if i == 4:
                    Qoe = "很好"
        return Qoe

    def showErrorGraph(self):
        print(min(self.error_history))
        showGraphWithIters(self.error_history)

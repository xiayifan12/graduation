from bp_for_qoe.Util.mathTools import rand, make_matrix, sigmoid
from bp_for_qoe.Setting.basesetting import NUM_OF_OUTPUT, NUM_OF_HIDDEN_LAYERS, NUM_OF_HIDDEN_LIST, NUM_OF_INPUT, LEARNING_RATE, \
    CORRECT_RATE, RANGE_UNDER, \
    RANGE_UPDER, FINAL_ERROR, MAX_TIME
from bp_for_qoe.Util.DataHandle import HandleLabel, MaxMinNormalization
from bp_for_qoe.Util.VisualizationTools import showGraphWithIters

'''
@Author:xiayifan
@Function:该模块定义了核心的bp神经网路类
@Update : 4/11 改变思路，将回归问题转换为分类问题
          4/14 准备在此分支重构代码
'''


# 核心bp神经网络类
class BPNeuralNetwork:
    def __init__(self):
        self.input_n = 0
        self.hidden_layer = 0
        self.hidden_n = []
        self.output_n = 0
        self.input_weight = []
        self.hidden_weight = []
        self.output_weight = []
        self.input_cells = []
        self.hidden_cells = []
        self.output_cells = []
        self.input_correction = []
        self.output_correction = []
        self.error_history = []
        self.maxNorm = []
        self.minNorm = []

    def start(self, ni, nhl, nh, no):
        self.input_n = ni + 1  # 输入层加一个偏置神经元
        self.hidden_layer = nhl  # 隐含层个数
        self.hidden_n = nh  # 隐含层
        self.output_n = no  # 输出层
        # 初始化神经元
        self.input_cells = [1.0] * self.input_n
        # self.hidden_cells = [1.0] * self.hidden_n
        self.output_cells = [1.0] * self.output_n
        for i in range(self.hidden_layer):
            hidden_cell = [1.0] * self.hidden_n[i]
            self.hidden_cells.append(hidden_cell)
        # 初始化权重（构造邻接矩阵）
        self.input_weight = make_matrix(self.input_n, self.hidden_n[0])  # 输入层与隐含层之间的权重
        for i in range(0,self.hidden_layer - 1,):  # 隐含层之间的权重
            hidden_weight_unit = make_matrix(self.hidden_n[i], self.hidden_n[i + 1])
            self.hidden_weight.append(hidden_weight_unit)
        self.output_weight = make_matrix(self.hidden_n[self.hidden_layer - 1], self.output_n)  # 隐含层与输出层之间的权重
        # 随机初始化权重
        for i in range(self.input_n):
            for h in range(self.hidden_n[0]):
                self.input_weight[i][h] = rand(RANGE_UNDER, RANGE_UPDER)

        for j in range(self.hidden_layer - 1):
            for k in range(self.hidden_n[j]):
                for m in range(self.hidden_n[j + 1]):
                    self.hidden_weight[j][k][m] = rand(RANGE_UNDER, RANGE_UPDER)

        for h in range(self.hidden_n[self.hidden_layer - 1]):
            for o in range(self.output_n):
                self.output_weight[h][o] = rand(RANGE_UNDER, RANGE_UPDER)
        # 初始化修正矩阵
        self.input_correction = make_matrix(self.input_n, self.hidden_n[0])
        self.output_correction = make_matrix(self.hidden_n[self.hidden_layer-1], self.output_n)

    def predict(self, inputs):  # 完成一次正向传播
        for i in range(self.input_n - 1):
            self.input_cells[i] = inputs[i]
        # 输入层
        for j in range(self.hidden_n[0]):
            total = 0.0
            for i in range(self.input_n):
                total += self.input_cells[i] * self.input_weight[i][j]
            self.hidden_cells[0][j] = sigmoid(total)
        # 隐含层
        for m in range(self.hidden_layer - 1):
            for h in range(self.hidden_n[m + 1]):
                total = 0.0
                for j in range(self.hidden_n[m]):
                    total += self.hidden_cells[m][j] * self.hidden_weight[m][j][h]
                self.hidden_cells[m + 1][h] = sigmoid(total)
        # 输出层
        for k in range(self.output_n):
            total = 0.0
            for j in range(self.hidden_n[self.hidden_layer - 1]):
                total += self.hidden_cells[self.hidden_layer - 1][j] * self.output_weight[j][k]
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
        # 初始化hidden误差
        hidden_deltas = []
        for i in range(self.hidden_layer):
            hidden_delta = [0.0] * self.hidden_n[i]
            hidden_deltas.append(hidden_delta)
        # 最后一层
        for h in range(self.hidden_n[self.hidden_layer - 1]):
            error = 0.0
            for o in range(self.output_n):
                error += output_deltas[o] * self.output_weight[h][o]
            hidden_deltas[self.hidden_layer - 1][h] = sigmoid(self.hidden_cells[self.hidden_layer - 1][h],
                                                              False) * error
        # 计算其他层hidden误差
        for k in range(self.hidden_layer - 2, -1, -1):
            for h in range(self.hidden_n[k]):
                error = 0.0
                for o in range(self.hidden_n[k + 1]):
                    error += hidden_deltas[k + 1][o] * self.hidden_weight[k][h][o]
                hidden_deltas[k][h] = sigmoid(self.hidden_cells[k][h], False) * error
        # 更新权重
        # 最后隐含层到输出层
        for h in range(self.hidden_n[self.hidden_layer - 1]):
            for o in range(self.output_n):
                change = output_deltas[o] * self.hidden_cells[self.hidden_layer - 1][h]
                # self.output_weight[h][o] += learn * change
                self.output_weight[h][o] += learn * change + correct * self.output_correction[h][o]
                self.output_correction[h][o] = change
        # 隐含层之间
        for m in range(self.hidden_layer - 2, -1, -1):
            for h in range(self.hidden_n[m]):
                for o in range(self.hidden_n[m + 1]):
                    change = hidden_deltas[m + 1][o] * self.hidden_cells[m][h]
                    self.hidden_weight[m][h][o] += learn * change
        # 输入层到第一隐含层
        for i in range(self.input_n):
            for h in range(self.hidden_n[0]):
                change = hidden_deltas[0][h] * self.input_cells[i]
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
        self.start(NUM_OF_INPUT, NUM_OF_HIDDEN_LAYERS, NUM_OF_HIDDEN_LIST, NUM_OF_OUTPUT)
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
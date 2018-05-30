from bp_for_qoe.Util.mathTools import rand, make_matrix, sigmoid
from bp_for_qoe.Setting.basesetting import NUM_OF_OUTPUT, NUM_OF_HIDDEN, NUM_OF_INPUT, LEARNING_RATE, CORRECT_RATE, \
    RANGE_UNDER, \
    RANGE_UPDER, FINAL_ERROR, MAX_TIME
from bp_for_qoe.Util.DataHandle import HandleLabel, MaxMinNormalization, reMaxMinNormalization, \
    useMaxMinNormalizationHandle
from bp_for_qoe.Util.VisualizationTools import showGraphWithIters
from bp_for_qoe.Util.excelHandle import InsertNNToExcel, GetNNFromExcel
from random import shuffle

'''
@Author:xiayifan
@Function:该模块定义了核心的bp神经网路类
@Update : 5/8 改变思路，依旧生成实数
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
        self.maxAtrNorm = []
        self.minAtrNorm = []
        self.maxLabNorm = 0
        self.minLabNorm = 0

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
        retrunAtrThings = MaxMinNormalization(casesR)
        cases = retrunAtrThings[0]
        # labels = HandleLabel(labelsR)
        returnLabelThings = useMaxMinNormalizationHandle(labelsR)
        labels = returnLabelThings[0]
        self.maxLabNorm = returnLabelThings[1]
        self.minLabNorm = returnLabelThings[2]
        self.maxAtrNorm = retrunAtrThings[1]
        self.minAtrNorm = retrunAtrThings[2]
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

    def forecase(self, delay, bandwidth, packet, jitter):

        caseR = [delay, bandwidth, packet, jitter]
        case = []
        for i in range(len(caseR)):
            x = (caseR[i] - self.minAtrNorm[i]) / (self.maxAtrNorm[i] - self.minAtrNorm[i])
            if x < 0:
                x = 0
            case.append(x)
        self.predict(case)
        result = reMaxMinNormalization(self.output_cells[0], self.maxLabNorm, self.minLabNorm)
        # result -= 0.05
        return result

    def showErrorGraph(self):
        print(min(self.error_history))
        showGraphWithIters(self.error_history)

    def saveNN(self):
        InsertNNToExcel([self.input_weight, self.output_weight], [self.maxAtrNorm, self.minAtrNorm],
                        [self.maxLabNorm, self.minLabNorm])

    def loadNN(self):
        self.start(NUM_OF_INPUT, NUM_OF_HIDDEN, NUM_OF_OUTPUT)
        matRaw = GetNNFromExcel()
        m = 0
        for k in self.input_weight:
            for h in range(len(k)):
                k[h] = matRaw[0][m]
                m = m + 1
        m = 0
        for k in self.output_weight:
            for h in range(len(k)):
                k[h] = matRaw[1][m]
                m = m + 1

        for i in range(NUM_OF_INPUT):
            self.maxAtrNorm.append(matRaw[2][i])

        for i in range(4, NUM_OF_INPUT + 4):
            self.minAtrNorm.append(matRaw[2][i])

        self.maxLabNorm = matRaw[3][0]
        self.minLabNorm = matRaw[3][1]

    def verify(self, caseR, labelR):
        self.loadNN()
        count = 0
        right = 0
        for i in range(len(caseR)):
            count += 1
            case = caseR[i]
            label = labelR[i][0]
            output = self.forecase(case[0], case[1], case[2], case[3])
            o = round(output, 2)
            label = round(label, 2)
            if o == label:
                right += 1
        # right = 1652
        # count = 2000
        p = right / count
        p = p * 100
        print("测试准确率：" + str(right) + "/" + str(count) + "----" + str(p) + "%")

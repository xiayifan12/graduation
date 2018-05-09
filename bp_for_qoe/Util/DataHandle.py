from bp_for_qoe.Setting.basesetting import *

'''
@Author:xiayifan
@Function: 1.对读取的原始文件输入进行归一化处理
           2.对读取的原始文件标签数据，进行人工分类



'''

'''
@函数功能：归一化初始数据集
@归一化标准：
          本次实验采用：最大-最小标准化
          目的：1.存在奇异样本，可能会导致训练失败
               2. 样本部分属性数值过大，可能导致激励函数等处理失败
          @input:[[RawAttr1,RawAttr2,RawAttr3,RawAttr4]....]
          @deal: x' = x- min / max - min
          @output: [[NormAttr1,NormAttr2,NormAttr3,NormAttr4]...]
'''


def MaxMinNormalization(casesR):
    attrsR = []
    for i in range(len(casesR[0])):
        attr = []
        attrsR.append(attr)
    for i in range(len(casesR)):
        caseR = casesR[i]
        for j in range(len(caseR)):
            attrsR[j].append(caseR[j])
    attrMax = []
    attrMin = []
    for i in range(len(attrsR)):
        attrMax.append(max(attrsR[i]))
        attrMin.append(min(attrsR[i]))
    cases = []
    for i in range(len(casesR)):
        case = []
        for j in range(len(casesR[i])):
            x = (casesR[i][j] - attrMin[j]) / (attrMax[j] - attrMin[j])
            case.append(x)
        cases.append(case)
    return [cases, attrMax, attrMin]


'''
@函数功能：量化qoe数据
@QoE划分分类规定：
                      数值                           服务质量
                            --- VERY_WORSE            很差
                VERY_WORSE  --- NORMAL                较差
                NORMAL      --- GOOD                  中档
                GOOD        ---- VERY_GOOD            较好
                VERY_GOOD   ----                      很好

        @Input：
                type: list
                format:[[QoE_RawNumber]...]

        @Output:
                type: list
                format:[[很差，较差，中档，较好，很好]...]
                value: 1表示选中  0表示未选中
                       五项中只有一项可以被选中
'''


def reMaxMinNormalization(labelR, max, min):
    return (max - min) * labelR + min


def useMaxMinNormalizationHandle(labelR):
    labs = []
    for l in labelR:
        labs.append(l[0])
    maxL = max(labs)
    minL = min(labs)
    labels = []
    for l in labs:
        y = (l - minL) / (maxL - minL)
        labels.append([y])
    return [labels, maxL, minL]


def HandleLabel(labelsR):
    labels = []
    for i in range(len(labelsR)):
        label = []
        if labelsR[i][0] <= VERY_WORSE:
            label = [1, 0, 0, 0, 0]
        if VERY_WORSE < labelsR[i][0] <= NORMAL:
            label = [0, 1, 0, 0, 0]
        if NORMAL < labelsR[i][0] <= GOOD:
            label = [0, 0, 1, 0, 0]
        if GOOD < labelsR[i][0] <= VERY_GOOD:
            label = [0, 0, 0, 1, 0]
        if labelsR[i][0] > VERY_GOOD:
            label = [0, 0, 0, 0, 1]
        labels.append(label)
    return labels

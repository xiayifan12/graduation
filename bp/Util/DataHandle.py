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
                      数值               服务质量
                0     --- 10000            很差
                10001  --- 15000           较差
                15001 --- 20000            中档
                20000 ---- 25000           较好
                25001以上                  很好

        @Input：
                type: list
                format:[[QoE_RawNumber]...]

        @Output:
                type: list
                format:[[很差，较差，中档，较好，很好]...]
                value: 1表示选中  0表示未选中
                       五项中只有一项可以被选中
'''


def HandleLabel(labelsR):
    labels = []
    for i in range(len(labelsR)):
        label = []
        if labelsR[i][0] <= 10000:
            label = [1, 0, 0, 0, 0]
        if 10000 < labelsR[i][0] <= 15000:
            label = [0, 1, 0, 0, 0]
        if 15000 < labelsR[i][0] <= 20000:
            label = [0, 0, 1, 0, 0]
        if 20000 < labelsR[i][0] <= 25000:
            label = [0, 0, 0, 1, 0]
        if labelsR[i][0] > 25000:
            label = [0, 0, 0, 0, 1]
        labels.append(label)
    return labels

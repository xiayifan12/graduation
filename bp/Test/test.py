from bp.Core.BPNeuralNetwork import BPNeuralNetwork
from bp.Util.excelHandle import GetDataSetAndLabelsFormExcel
from bp.Util.DataHandle import MaxMinNormalization, HandleLabel

if __name__ == '__main__':
    QoeModel = BPNeuralNetwork()
    casesR = GetDataSetAndLabelsFormExcel()[0]
    labelsR = GetDataSetAndLabelsFormExcel()[1]
    QoeModel.test(casesR, labelsR)
    re = QoeModel.forecase(4.554, 26177, 2499879, 0)
    print(re)

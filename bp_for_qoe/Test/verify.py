from bp_for_qoe.Core.QoEAss import BPNeuralNetwork
from bp_for_qoe.Util.excelHandle import GetDataSetAndLabelsFormExcel

if __name__ == '__main__':
    QoeModel = BPNeuralNetwork()
    casesR = GetDataSetAndLabelsFormExcel()[0]
    labelsR = GetDataSetAndLabelsFormExcel()[1]
    QoeModel.verify(casesR, labelsR)

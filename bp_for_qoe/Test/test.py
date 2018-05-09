from bp_for_qoe.Core.QoEAss import BPNeuralNetwork
from bp_for_qoe.Util.excelHandle import GetDataSetAndLabelsFormExcel
import bp_for_qoe.Core.multiplehidden as cp

if __name__ == '__main__':
    QoeModel = BPNeuralNetwork()
    # casesR = GetDataSetAndLabelsFormExcel()[0]
    # labelsR = GetDataSetAndLabelsFormExcel()[1]
    # QoeModel.test(casesR, labelsR)
    # QoeModel.showErrorGraph()
    QoeModel.loadNN()
    # while True:
    #     a = input("1:")
    #     b = input("2:")
    #     c = input("3:")
    #     d = input("4:")
    #     print(QoeModel.forecase(float(a), float(b), float(c), float(d)))
    #     o = input("over?")
    #     if o == 'yes':
    #         break

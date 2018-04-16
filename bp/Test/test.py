from bp.Core.BPNeuralNetwork import BPNeuralNetwork
from bp.Util.excelHandle import GetDataSetAndLabelsFormExcel
import bp.Core.CopyByBp as cp

if __name__ == '__main__':
    QoeModel = cp.BPNeuralNetwork()
    casesR = GetDataSetAndLabelsFormExcel()[0]
    labelsR = GetDataSetAndLabelsFormExcel()[1]
    QoeModel.test(casesR, labelsR)
    QoeModel.showErrorGraph()
    # while True:
    #     a = input("1:")
    #     b = input("2:")
    #     c = input("3:")
    #     d = input("4:")
    #     print(QoeModel.forecase(float(a), float(b), float(c), float(d)))
    #     o = input("over?")
    #     if o == 'yes':
    #         break

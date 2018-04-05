from bp.Util.excelHandle import GetDataSetAndLabelsFormExcel
from bp.Core.BPNeuralNetwork import BPNeuralNetwork


if __name__ != '__main__':
    QoEassmodel = BPNeuralNetwork()
    cases = GetDataSetAndLabelsFormExcel()[0]
    labels = GetDataSetAndLabelsFormExcel()[1]
    QoEassmodel.test(cases, labels)
    print("********************************")
    print("神经网络训练完毕! QoE评价模型准备就绪！")
    print("********************************")
    while True:
        delay = input("请输入网络延迟：")
        shake = input("请输入网络抖动:")
        packet = input("请输入丢包率:")
        bandwidth = input("请输入网络带宽:")
        print("***********少女祈祷中************")
        print("QoE评价结果为：")
        print(QoEassmodel.forecase(delay, shake, packet, bandwidth))
        print("***********少女祈祷中************")
        flag = input("是否退出QoE预测模型程序？")
        if flag == 'YES':
            break
    print("QoE预测程序结束......")
else:
    print("hello")
    QoeModel = BPNeuralNetwork()
    cases = GetDataSetAndLabelsFormExcel()[0]
    labels = GetDataSetAndLabelsFormExcel()[1]
    print(cases[0][1])
    QoeModel.test(cases, labels)
    print("********************************")
    print("神经网络训练完毕! QoE评价模型准备就绪！")
    print("********************************")
    a = input("1:")
    b = input("2:")
    c = input("3:")
    d = input("4:")
    print(QoeModel.forecase(float(a),float(b),float(c),float(d)))
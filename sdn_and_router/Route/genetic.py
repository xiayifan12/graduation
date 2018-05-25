from operator import attrgetter
from sdn_and_router.Route.base import *
from bp_for_qoe.Core.QoEAss import BPNeuralNetwork
from random import random, sample, shuffle, seed
from sdn_and_router.Support.graphHandel import getIFs
import matplotlib.pyplot as plt

'''全局变量定义'''
popInitPath = []  # 用于初始化基因型集合
'''
遗传算法本体
'''


def genetic(graph, topy, src, dst):
    individual.QoEassInit()
    bestindivitions = []
    initpop = create_pop(graph, topy, src, dst)  # 随机一点！！！
    seed()
    pop = sample(initpop, POP_SIZE)
    for i in range(MAX_GENARATION):
        sortkey = attrgetter('phenotype')
        bestsortlist = pop
        bestsortlist.sort(key=sortkey, reverse=True)
        bestindivition = bestsortlist[0]
        bestindivitions.append(bestindivition)
        # if bestindivition.phenotype > xxxx
        #     break
        selecpop = selection(pop)
        shuffle(selecpop)
        cropop = crossover(selecpop, graph, topy)
        # cropop.append(bestindivition)
        mutapop = mutation(cropop, graph, topy)
        pop = mutapop
        pop.append(bestindivition)
    showlist = []
    for i in bestindivitions:
        showlist.append(i.phenotype)
    print(max(showlist))
    sortkey = attrgetter('phenotype')
    bestindivitions.sort(key=sortkey, reverse=True)
    print(bestindivitions[0].genotype)
    plt.plot(showlist)
    plt.title('Best QoE in pop')
    plt.xlabel('pop_num')
    plt.ylabel('QoE by MOS')
    plt.ylim(4.600, 5.000)
    plt.xlim(0, 20)
    plt.show()


'''
类：用于储存基因型以及其对应表现型 
'''


class individual:
    def __init__(self):
        self.genotype = []
        self.phenotype = 0.0
        self.fit = 0.0
        self.leftFit = 0.0
        self.rightFit = 0.0

    QoEAss = BPNeuralNetwork()

    @classmethod
    def QoEassInit(self):
        individual.QoEAss.loadNN()

    def decoding(self, graph):
        ifs = getIFs(self.genotype, graph)
        self.phenotype = individual.QoEAss.forecase(ifs[0], ifs[1], ifs[2], ifs[3])

    def start(self, gen, graph):
        self.genotype = gen
        self.decoding(graph)

    def countFit(self, sum):
        self.fit = (self.phenotype / sum)

    def countRange(self, left, right):
        self.leftFit = left
        self.rightFit = right


'''
编码：采用不等长实数编码的形式,以路径点序号作为基因序列
'''


def encodeing(route):
    return route


'''
初始化种群:通过深度优先搜索，找到M条从起点到终点的路径作为初始种群
'''


def create_pop(graph, topy, src, dst):
    popInitPath.clear()
    visted = []
    dfsForPop(src, topy, visted, dst)
    popEncodingList = encodeing(popInitPath)
    popList = []
    for ls in popEncodingList:
        i = individual()
        i.start(ls, graph)
        popList.append(i)
    return popList


def dfsForPop(node, graph, visited, dst):
    V = []
    V = visited
    if len(popInitPath) >= POP_SELECT_SIZE:
        return
    V.append(node)
    if node == dst:
        popInitPath.append(V)
        return
    for i in range(len(graph[node])):
        if graph[node][i] == 1 and i not in V:
            fordigui = V.copy()
            dfsForPop(i, graph, fordigui, dst)
    return


'''
选择
'''


def sumOfFit(popList):
    sum = 0.0
    for i in popList:
        sum += i.phenotype
    return sum


def selection(pop):
    sum = sumOfFit(pop)
    pre = 0.0
    for i in pop:
        i.countFit(sum)
        i.countRange(pre, pre + i.fit)
        pre = pre + i.fit
    randomValue = []
    seed()
    for i in range(len(pop)):
        randomValue.append(random())
    randomValue.sort()
    newpop = []
    for i in randomValue:
        for j in pop:
            if j.leftFit < i <= j.rightFit:
                newpop.append(j)
                break
    return newpop


'''
交叉:
'''


def switchByPoint(father, mother, fp, mp, graph):
    temp1 = father.genotype[:fp] + mother.genotype[mp:]
    temp2 = mother.genotype[:mp] + father.genotype[fp:]
    t1 = individual()
    t1.start(temp1, graph)
    clearCircle(t1, graph)
    t2 = individual()
    t2.start(temp2, graph)
    clearCircle(t2, graph)
    return [t1, t2]


def switchByTonari(father, mother, fp, mp, graph):
    temp1 = father.genotype[:fp] + mother.genotype[mp:]
    t1 = individual()
    t1.start(temp1, graph)
    clearCircle(t1, graph)
    return t1


def goodGen(father, mother):
    if father.phenotype >= mother.phenotype:
        return father
    else:
        return mother


def clearCircle(newpopIndiv, graph):
    for i in range(len(newpopIndiv.genotype)):
        if newpopIndiv.genotype.count(newpopIndiv.genotype[i]) > 1 and newpopIndiv.genotype[i] != -1:
            for j in range(i + 1, len(newpopIndiv.genotype)):
                if newpopIndiv.genotype[j] == newpopIndiv.genotype[i]:
                    newpopIndiv.genotype[j] = -1
                    break
                else:
                    newpopIndiv.genotype[j] = -1
    for i in range(len(newpopIndiv.genotype)):
        if newpopIndiv.genotype.count(-1) > 0:
            newpopIndiv.genotype.remove(-1)
        else:
            break
    newpopIndiv.decoding(graph)


def crossover(pop, graph, topy):
    newpop = []
    for i in range(len(pop) - 1):
        flag_point = 0
        flag_tonari = 0
        flag_point_father = 0
        flag_tonari_father = 0
        flag_point_monther = 0
        flag_tonari_monther = 0
        seed()
        if random() < PROBABILITY_CROSSOVER:
            for j in range(1, len(pop[i].genotype) - 1):
                for k in range(1, len(pop[i + 1].genotype) - 1):
                    if pop[i].genotype[j] == pop[i + 1].genotype[k] and flag_point == 0:
                        flag_point = 1
                        flag_point_father = j
                        flag_point_monther = k
                    if flag_tonari == 0 and topy[pop[i].genotype[j]][pop[i + 1].genotype[k]] == 1:
                        flag_tonari = 1
                        flag_tonari_father = j
                        flag_tonari_monther = k
                    if flag_point == 1 and flag_tonari == 1:
                        break
                if flag_point == 1 and flag_tonari == 1:
                    break
            if flag_tonari == 1 and flag_point == 1:
                if random() < PROBABILITY_CROSSOVER_SELECTION:
                    rel = switchByPoint(pop[i], pop[i + 1], flag_point_father, flag_point_monther, graph)
                    clearCircle(rel[0], graph)
                    clearCircle(rel[1], graph)
                    gg = goodGen(rel[0], rel[1])
                    newpop.append(gg)
                    # newpop.append(rel[0])
                    # newpop.append(rel[1])
                else:
                    rel = switchByTonari(pop[i], pop[i + 1], flag_tonari_father, flag_tonari_monther, graph)
                    clearCircle(rel, graph)
                    newpop.append(rel)
                    # newpop.append(goodGen(pop[i], pop[i + 1]))
            elif flag_point == 0 and flag_point == 1:
                rel = switchByPoint(pop[i], pop[i + 1], flag_point_father, flag_point_monther, graph)
                clearCircle(rel[0], graph)
                clearCircle(rel[1], graph)
                newpop.append(rel[0])
                newpop.append(rel[1])
            elif flag_point == 1 and flag_point == 0:
                rel = switchByTonari(pop[i], pop[i + 1], flag_tonari_father, flag_tonari_monther, graph)
                clearCircle(rel, graph)
                newpop.append(rel)
                newpop.append(goodGen(pop[i], pop[i + 1]))
            else:
                newpop.append(pop[i])
                newpop.append(pop[i + 1])
        else:
            gg = goodGen(pop[i], pop[i + 1])
            newpop.append(gg)
            # newpop.append(pop[i])
            # newpop.append(pop[i + 1])

    return newpop


'''
基因突变：
'''


def dfsForMutation(node, dst, graph, visited, orig, src):
    path = []
    visited.append(node)
    V = visited.copy()
    if node == dst:
        index = 0
        for i in range(len(V)):
            if V[i] != src:
                continue
            else:
                index = i
                break
        V = V[index:]
        V.reverse()
        path = V.copy()
        orig.append(src)
        if path != orig:
            return path
    for i in range(len(graph[node])):
        if graph[node][i] == 1 and i not in visited:
            V = visited.copy()
            path = dfsForMutation(i, dst, graph, V, orig, src)
            V = visited.copy()
            if path:
                break
    return path


def mutation(pop, graph, topy):
    newpop = []
    for i in pop:
        seed()
        if random() < PROBABILITY_MUTATION:
            seleclist = i.genotype[1:len(i.genotype) - 1]
            while seleclist:
                gen = sample(seleclist, 1)[0]
                index = 0
                for j in range(len(i.genotype)):
                    if i.genotype[j] == gen:
                        index = j
                        break
                orilist = i.genotype[:index]
                visited = i.genotype[index + 1:]
                addcp = visited.copy()
                path = dfsForMutation(gen, i.genotype[0], topy, visited, orilist, gen)
                for p in addcp:
                    path.append(p)
                if path:
                    newi = individual()
                    newi.start(path, graph)
                    newpop.append(newi)
                    break
                seleclist.remove(gen)
            if not seleclist:
                newpop.append(i)
        else:
            newpop.append(i)
    return newpop

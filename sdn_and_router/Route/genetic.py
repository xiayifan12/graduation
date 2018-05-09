from operator import attrgetter
from sdn_and_router.Route.base import *
from bp_for_qoe.Core.BPNeuralNetwork import BPNeuralNetwork
from random import random, sample

'''全局变量定义'''
popInitPath = []  # 用于初始化基因型集合
QoEAss = BPNeuralNetwork()
'''
遗传算法本体
'''


def genetic(graph, src, dst):
    bestindivitions = []
    initpop = create_pop(graph, src, dst)
    pop = initpop
    for i in range(MAX_GENARATION):
        sortkey = attrgetter('phenotype')
        bestsortlist = pop
        bestsortlist.sort(key=sortkey)
        bestindivition = bestsortlist[0]
        bestindivitions.append(bestindivition)
        # if bestindivition.phenotype > xxxx
        #     break
        selecpop = selection(initpop)
        cropop = crossover(selecpop, graph)
        mutapop = mutation(cropop, graph)
        pop = mutapop


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

    def decoding(self):
        return
        # width = getWidthFromPath()
        # delay = getDelayFromPath()
        # jitter = getJitterFromPath()
        # packet = getPacketFromPath()
        # self.phenotype = QoEAss.forecase()

    def start(self, gen):
        self.genotype = gen
        self.phenotype = 0.0

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


def create_pop(graph, src, dst):
    popInitPath.clear()
    visted = []
    dfsForPop(src, graph, visted, dst)
    popEncodingList = encodeing(popInitPath)
    popList = []
    for ls in popEncodingList:
        i = individual()
        i.start(ls)
        popList.append(i)
    return popList


def dfsForPop(node, graph, visited, dst):
    if len(popInitPath) >= POP_SIZE:
        return
    visited.append(node)
    if node == dst:
        popInitPath.append(visited)
        return
    for extend in graph[node]:
        if extend == 1 and extend not in visited:
            dfsForPop(extend, graph, visited, dst)
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
        i.contFit(sum)
        i.countRange(pre, pre + i.fit)
        pre = pre + i.fit
    randomValue = []
    for i in range(len(pop)):
        randomValue.append(random())
    randomValue.sort()
    newpop = []
    for i in randomValue:
        for j in pop:
            if j.leftFit < i <= j.rightFit:
                newpop.append(i)
                break
    return newpop


'''
交叉:
'''


def switchByPoint(father, mother, fp, mp):
    temp1 = father.genotype[:fp] + mother.genotype[mp:]
    temp2 = mother.genotype[:mp] + father.genotype[fp:]
    t1 = individual()
    t1.start(temp1)
    t2 = individual()
    t2.start(temp2)
    return [t1, t2]


def switchByTonari(father, mother, fp, mp):
    temp1 = father.genotype[:fp] + mother.genotype[mp:]
    t1 = individual()
    t1.start(temp1)
    return t1


def goodGen(father, mother):
    if father.phenotype >= mother.phenotype:
        return father
    else:
        return mother


def clearCircle(newpopIndiv):
    for i in range(len(newpopIndiv.genotype)):
        if newpopIndiv.genotype.count(newpopIndiv.genotype[i]) > 1:
            for j in range(i + 1, len(newpopIndiv.genotype)):
                if newpopIndiv.genotype[j] == newpopIndiv.genotype[i]:
                    del newpopIndiv.genotype[j]
                    break
                else:
                    del newpopIndiv.genotype[j]


def crossover(pop, graph):
    newpop = []
    for i in range(len([pop]) - 1):
        flag_point = 0
        flag_tonari = 0
        flag_point_father = 0
        flag_tonari_father = 0
        flag_point_monther = 0
        flag_tonari_monther = 0
        if random() < PROBABILITY_CROSSOVER:
            for j in range(1, len(pop[i]) - 1):
                for k in range(1, len(pop[i + 1]) - 1):
                    if pop[i].genotype[j] == pop[i + 1].genotype[k] and flag_point == 0:
                        flag_point = 1
                        flag_point_father = j
                        flag_point_monther = k
                    if flag_tonari == 0 and graph[pop[i].genotype[j]][pop[i + 1].genotype[k]] == 1:
                        flag_tonari = 1
                        flag_tonari_father = j
                        flag_tonari_monther = k
            if flag_tonari == 1 and flag_point == 1:
                if random() < PROBABILITY_CROSSOVER_SELECTION:
                    rel = switchByPoint(pop[i], pop[i + 1], flag_point_father, flag_point_monther)
                    clearCircle(rel[0])
                    clearCircle(rel[1])
                    newpop.append(rel[0])
                    newpop.append(rel[1])
                else:
                    rel = switchByTonari(pop[i], pop[i + 1], flag_tonari_father, flag_tonari_monther)
                    clearCircle(rel)
                    newpop.append(rel)
                    newpop.append(goodGen(pop[i], pop[i + 1]))
            elif flag_point == 0 and flag_point == 1:
                rel = switchByPoint(pop[i], pop[i + 1], flag_point_father, flag_point_monther)
                clearCircle(rel[0])
                clearCircle(rel[1])
                newpop.append(rel[0])
                newpop.append(rel[1])
            elif flag_point == 1 and flag_point == 0:
                rel = switchByTonari(pop[i], pop[i + 1], flag_tonari_father, flag_tonari_monther)
                clearCircle(rel)
                newpop.append(rel)
                newpop.append(goodGen(pop[i], pop[i + 1]))
            else:
                newpop.append(pop[i])
                newpop.append(pop[i + 1])
        else:
            newpop.append(pop[i])
            newpop.append(pop[i + 1])

    return newpop


'''
基因突变：
'''


def dfsForMutation(node, dst, graph, visited, orig):
    path = None
    visited.append(node)
    if node == dst:
        path = visited.reverse()
        if path != orig:
            return path
    for i in graph[node]:
        if graph[node][i] == 1:
            path = dfsForMutation(i, dst, graph, visited, orig)
            if path is not None:
                break
    return path


def mutation(pop, graph):
    newpop = []
    for i in pop:
        if random < PROBABILITY_MUTATION:
            seleclist = i.genotype[1:len(i.genotype) - 1]
            while seleclist:
                gen = sample(seleclist, 1)
                orilist = i.genotype[:gen]
                visited = i.genotype[gen:]
                path = dfsForMutation(gen, i.genotype[0], graph, visited, orilist)
                if path is not None:
                    newi = individual()
                    newi.start(path)
                    newpop.append(newi)
                    break
                seleclist.remove(gen)
            if seleclist is None:
                newpop.append(i)
        else:
            newpop.append(i)
    return newpop

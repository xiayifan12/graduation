from sdn_and_router.Support.graphHandel import getGraph, randomGraph
from sdn_and_router.Route.genetic import genetic, individual
from sdn_and_router.Route.base import SOURCE_NODE, DST_NODE
from sdn_and_router.Route.dijkstra import dijkstra
from random import randint, seed, sample
import matplotlib as mpl
from copy import deepcopy
import matplotlib.pyplot as plt

if __name__ == '__main__':
    grap = getGraph()
    randomGraph(grap[0], grap[1])
    x_qoe = []
    x_dj = []
    # seed()
    # src = randint(0, 12)
    # dst = randint(0, 12)
    # while src == dst:
    #     seed()
    #     dst = randint(0, 12)
    # genetic(grap[0], grap[1], src, dst)
    # duibi = dijkstra(grap[1], src, dst)
    for i in range(10):
        seed()
        # randomGraph(grap[0], grap[1])
        # seed()
        select1 = [0, 5, 6, 4, 10, 7]
        select2 = {1, 8, 12, 11, 2, 9, 3}
        src = sample(select1, 1)[0]
        dst = sample(select2, 1)[0]
        # src = SOURCE_NODE
        # dst = DST_NODE
        gdist = []
        for j in range(10):
            g = genetic(grap[0], grap[1], src, dst)
            g -= 0.1
            gdist.append(g)
        gm = max(gdist)
        duibitu = deepcopy(grap[1])
        duibi = dijkstra(duibitu, src, dst)
        duibiI = individual()
        duibiI.start(duibi, grap[0])
        d = duibiI.phenotype
        d -= 0.1
        x_qoe.append(gm)
        x_dj.append(d)
    plt.xlabel('experiment times')
    plt.ylabel('QoE level')
    plt.plot(x_qoe, color='green', label='QoE optimization algorithm ')
    plt.plot(x_dj, color='red', label='Dijkstra algorithm', linewidth=1, linestyle='-.')
    plt.legend()  # 显示图例
    plt.ylim(4, 5)
    plt.show()
    # print(duibi)
    # duibiI = individual()
    # duibiI.start(duibi, grap[0])
    # print(duibiI.phenotype)

from sdn_and_router.Support.graphHandel import getGraph,randomGraph
from sdn_and_router.Route.genetic import genetic, individual
from sdn_and_router.Route.base import SOURCE_NODE, DST_NODE
from sdn_and_router.Route.dijkstra import dijkstra

if __name__ == '__main__':
    grap = getGraph()
    randomGraph(grap[0], grap[1])
    genetic(grap[0], grap[1], SOURCE_NODE, DST_NODE)
    duibi = dijkstra(grap[1], SOURCE_NODE, DST_NODE)
    print(duibi)
    duibiI = individual()
    duibiI.start(duibi, grap[0])
    print(duibiI.phenotype)

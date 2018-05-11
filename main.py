from sdn_and_router.Support.graphHandel import getGraph
from sdn_and_router.Route.genetic import genetic
from sdn_and_router.Route.base import SOURCE_NODE, DST_NODE

if __name__ == '__main__':

    grap = getGraph()
    genetic(grap[0], grap[1], SOURCE_NODE, DST_NODE)

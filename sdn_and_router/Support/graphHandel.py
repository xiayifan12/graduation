import xlrd

PATH = './sdn_and_router/static/hushuo.xlsx'


class graphNodes:
    def __init__(self):
        self.delay = 0.0
        self.width = 0.0
        self.packet = 0.0
        self.jitter = 0.0


def makeGraph(size):
    mat = []
    for i in range(size):
        p = []
        mat.append(p)


def getGraph():
    workbook = xlrd.open_workbook(PATH)
    sheet = workbook.sheet_by_index(0)
    row = sheet.nrows
    col = sheet.ncols
    graph = []
    graph_topy = []
    for i in range(row):
        grap = []
        grap_topy = []
        for j in range(col):
            tp = 0
            sr = str(sheet.row(i)[j].value)
            sp = sr.split(',')
            gr = graphNodes()
            gr.delay = float(sp[0])
            gr.width = float(sp[1])
            gr.packet = float(sp[2])
            gr.jitter = float(sp[3])
            if gr.width > 0:
                tp = 1
            grap.append(gr)
            grap_topy.append(tp)
        graph.append(grap)
        graph_topy.append(grap_topy)
    return [graph, graph_topy]


def getIFs(path, graph):
    delay = 0
    wid = 9999999
    packet = 0.0
    jitter = 0
    for i in range(len(path) - 1):
        delay += graph[path[i]][path[i + 1]].delay
        packet += graph[path[i]][path[i + 1]].packet
        jitter += graph[path[i]][path[i + 1]].jitter
        if graph[path[i]][path[i + 1]].width < wid:
            wid = graph[path[i]][path[i + 1]].width
    return [delay, wid, packet, jitter]

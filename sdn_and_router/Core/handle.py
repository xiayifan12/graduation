from sdn_and_router.Support.httptools import *
from sdn_and_router.Bean.unit import Link, Switch
from bp_for_qoe.Core.multiplehidden import BPNeuralNetwork
from bp_for_qoe.Util.mathTools import make_matrix
from sdn_and_router.Core.routeAlgo import dijkstra

'''
@Author:xiayifan
@Function:该模块定义了SDN北向REST接口的处理,包括路由发现，链路状态获取，路由优化策略
@Update :

'''


def checkAllFlow():
    res = doHTTP('GET', LIST_ALL_FLOW, GET_BODY)
    print(res)


def clearAllFlow():
    res = doHTTP('GET', CLEAR_ALL_FLOW, GET_BODY)
    print(res)


def getBandwidthByLink(link):
    switch = link.src_switch
    port = link.src_port
    URL = GET_BANDWIDTH + switch + '/' + str(port) + '/' + 'json'
    return doHTTP('GET', URL, GET_BODY)


def getBandwidthBySB(switch, port):
    URL = GET_BANDWIDTH + switch + '/' + str(port) + '/' + 'json'
    res = doHTTP('GET', URL, GET_BODY)
    return res


def getDelayBySB(switch, port):
    res = doHTTP('GET', GET_LINK_URL, GET_BODY)
    for lk in res:
        if lk['src-switch'] == switch and lk['src-port'] == str(port):
            return lk['latency']


def getDelayByLink(link):
    res = doHTTP('GET', GET_LINK_URL, GET_BODY)
    for lk in res:
        if lk['src-switch'] == link.src_switch and lk['src-port'] == link.src_port:
            return lk['latency']


class handle:
    def __init__(self):
        self.switchList = []
        self.hostList = []
        self.linkList = []
        self.topy = []
        self.flowseq = 0
        self.QoEAss = ''

    def start(self):
        self.getALLSwitchFromSDN()
        self.getALLLinkFromSDN()
        self.getDeviceFrom()
        self.topy = make_matrix(len(self.switchList), len(self.switchList), 0)
        self.makeTopy()
        self.QoEAss = BPNeuralNetwork()
        # BP网络从excel中提取矩阵,QoEAss.xxx()

    def switchSeqReflection(self, dpid):
        for i in range(len(self.switchList)):
            if self.switchList[i].pid == dpid:
                return i

    def getPath(self, method='dijkstra'):
        if method == 'dijkstra':
            cp = self.topy
            path = dijkstra(cp, self.switchSeqReflection(SCR_SWITCH), self.switchSeqReflection(DST_SWITCH))
            return path

    def dispathRouter(self):
        path = self.getPath()
        for i in range(len(path)):
            if i < len(path) - 1:
                self.addFlowByRoute(self.switchList[path[i]].pid, self.switchList[path[i + 1]].pid)
        self.addFlowInSwitch(self.switchList[path[len(path) - 1]].pid)

    def makeTopy(self):
        for lk in self.linkList:
            scrseq = self.switchSeqReflection(lk.getScrSw())
            dstseq = self.switchSeqReflection(lk.getDstSw())
            self.topy[scrseq][dstseq] = 1
            self.topy[dstseq][scrseq] = 1

    def getALLSwitchFromSDN(self):
        res = doHTTP('GET', GET_SWITCH_URL, GET_BODY)
        for sw in res:
            s = Switch()
            s.pid = sw['switchDPID']
            self.switchList.append(s)

    def getALLLinkFromSDN(self):
        res = doHTTP('GET', GET_LINK_URL, GET_BODY)
        for lk in res:
            l = Link()
            l.setDelay(lk['latency'])
            l.setScrSw(lk['src-switch'])
            l.setScrPt(lk['src-port'])
            l.setDstSw(lk['dst-switch'])
            l.setDstPt(lk['dst-port'])
            self.linkList.append(l)

    def getDeviceFrom(self):
        res = doHTTP('GET', DEVICE_SHOW, GET_BODY)
        device = res['devices']
        for dec in device:
            point = dec['attachmentPoint']
            if point:
                for sw in self.switchList:
                    if point[0]['switch'] == sw.pid:
                        sw.inport = int(point[0]['port'])
                        sw.outport = int(point[0]['port'])
                        sw.isEdge = True

    def addFlowByRoute(self, sw1, sw2):  # 下发sw1到sw2的路径流表
        body = {}
        rebody = {}
        switch = ''
        name = 'flow-mod-' + str(self.flowseq)
        self.flowseq += 1
        cookie = '0'
        priority = '32768'
        active = 'true'
        in_port = ''
        actions = ''
        re_in_port = ''
        re_action = ''
        s1 = ''
        s2 = ''
        for s in self.switchList:
            if s.pid == sw1:
                s1 = s
            if s.pid == sw2:
                s2 = s

        for lk in self.linkList:
            if lk.getScrSw() == sw1 and lk.getDstSw() == sw2:
                switch = s1.pid
                in_port = str(s1.inport)
                re_in_port = str(lk.getScrPt())
                actions = 'output=' + str(lk.getScrPt())
                re_action = 'output=' + str(s1.inport)
                s1.outport = lk.getScrPt()
                s2.inport = lk.getDstPt()
                break
            if lk.getScrSw() == sw2 and lk.getDstSw() == sw1:
                switch = s1.pid
                in_port = str(s1.inport)
                re_in_port = str(lk.getDstPt())
                actions = 'output=' + str(lk.getDstPt())
                re_action = 'output=' + str(s1.inport)
                s1.outport = lk.getDstPt()
                s2.inport = lk.getScrPt()
                break

        body['name'] = name
        body['switch'] = switch
        body['cookie'] = cookie
        body['priority'] = priority
        body['active'] = active
        body['in_port'] = in_port
        body['actions'] = actions
        data = body
        rebody['name'] = 'flow-mod-' + str(self.flowseq)
        rebody['switch'] = switch
        rebody['cookie'] = cookie
        rebody['priority'] = priority
        rebody['active'] = active
        rebody['in_port'] = re_in_port
        rebody['actions'] = re_action
        self.flowseq += 1
        doHTTP('POST', ADD_FLOW_URL, rebody)
        return doHTTP('POST', ADD_FLOW_URL, data)

    def addFlowInSwitch(self, sw):
        swch = ''
        body = {}
        rebody = {}
        name = 'flow-mod-' + str(self.flowseq)
        self.flowseq += 1
        cookie = '0'
        priority = '32768'
        active = 'true'
        for s in self.switchList:
            if s.pid == sw:
                swch = s

        switch = swch.pid
        in_port = str(swch.inport)
        re_in_port = str(swch.outport)
        actions = 'output=' + str(swch.outport)
        re_action = 'output=' + str(swch.inport)
        body['name'] = name
        body['switch'] = switch
        body['cookie'] = cookie
        body['priority'] = priority
        body['active'] = active
        body['in_port'] = in_port
        body['actions'] = actions
        data = body
        rebody['name'] = 'flow-mod-' + str(self.flowseq)
        rebody['switch'] = switch
        rebody['cookie'] = cookie
        rebody['priority'] = priority
        rebody['active'] = active
        rebody['in_port'] = re_in_port
        rebody['actions'] = re_action
        self.flowseq += 1
        doHTTP('POST', ADD_FLOW_URL, rebody)
        return doHTTP('POST', ADD_FLOW_URL, data)


if __name__ == '__main__':
    a = 0
    hd = handle()
    hd.start()
    clearAllFlow()
    hd.dispathRouter()
    # clearAllFlow()
    # hd.addFlowByRoute('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:03')
    # hd.addFlowInSwitch('00:00:00:00:00:00:00:03')
    print(getBandwidthBySB(switch, port))

    # hd.getALLLinkFromSDN()
    # hd.addFlowToSwitch('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:02')
    # data1 = {
    #     'switch': "00:00:00:00:00:00:00:03",
    #     "name": "flow-mod-1",
    #     "cookie": "0",
    #     "priority": "32768",
    #     "in_port": "1",
    #     "active": "true",
    #     "actions": "output=2"
    # }
    #
    # data2 = {
    #     'switch': "00:00:00:00:00:00:00:03",
    #     "name": "flow-mod-2",
    #     "cookie": "0",
    #     "priority": "32768",
    #     "in_port": "2",
    #     "active": "true",
    #     "actions": "output=1"
    # }
    # # doHTTP('POST', ADD_FLOW_URL, data2)
    # checkAllFlow()

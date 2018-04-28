from sdn_and_router.Support.httptools import *
from sdn_and_router.Bean.unit import Link, Switch

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


class handle:
    def __init__(self):
        self.switchList = []
        self.hostList = []
        self.linkList = []
        self.flowseq = 0

    def start(self):
        self.getALLSwitchFromSDN()
        self.getALLLinkFromSDN()
        self.getDeviceFrom()

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
    # clearAllFlow()
    # hd.addFlowByRoute('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:03')
    # hd.addFlowInSwitch('00:00:00:00:00:00:00:03')
    while True:
        contr = input("fuck:")
        if contr == 0:
            break

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

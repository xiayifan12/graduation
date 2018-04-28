class Link:
    def __init__(self):
        self.src_switch = ''
        self.dst_switch = ''
        self.src_port = -1
        self.dst_port = -1
        self.width = 0.0
        self.packet = 0.0
        self.delay = 0.0
        self.jitter = 0.0

    def getScrSw(self):
        return self.src_switch

    def getDstSw(self):
        return self.dst_switch

    def getScrPt(self):
        return self.src_port

    def getDstPt(self):
        return self.dst_port

    def getWid(self):
        return self.width

    def getPacket(self):
        return self.packet

    def getDelay(self):
        return self.delay

    def getJitter(self):
        return self.jitter

    def setScrSw(self, sc):
        self.src_switch = sc

    def setDstSw(self, dr):
        self.dst_switch = dr

    def setScrPt(self, sc):
        self.src_port = sc

    def setDstPt(self, dr):
        self.dst_port = dr

    def setWid(self, wd):
        self.width = wd

    def setPacket(self, pk):
        self.packet = pk

    def setDelay(self, de):
        self.delay = de

    def setJitter(self, jt):
        self.jitter = jt


class Switch:
    def __init__(self):
        self.pid = ''
        self.inport = -1
        self.outport = -1
        self.flow = []
        self.isEdge = False

    def getOutport(self):
        return self.outport

    def getInport(self):
        return self.inport

    def setInport(self, inp):
        self.inport = inp

    def setOutport(self, outp):
        self.outport = outp



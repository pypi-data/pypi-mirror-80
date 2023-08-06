from math import sqrt
from copy import deepcopy

from .optCells import *
from .legacy import  *
#from config import dfoptwgwidth, _index, dfOpeningLength, dfOpeningWidth, dfOpeningConnection, dfOpeningOffset, dfSkipPathNodes
# The above import won't be sync'ed globally, and only take the value initionalized and not follew the change.

from . import config
from .optCells import _normalizedxdy

def _pointDist(a, b):
    return sqrt(float(a[0] - b[0]) ** 2 + float(a[1] - b[1]) ** 2)


class SuspendOptStraightWaveguide(OptStraightWaveguide):
    """
    Straight waveguide with Openings

    Args:
        name: str
        inports: List[Tuple[float, float, float, float]]
        length: float
        layer: int
        endwidth: float

          *default* or *endwidth < 0 *, the waveguide width will keep unchanged.
          *endwidth >= 0.*, the waveguide width will be linearly tapered to *endwidth*

          **Note:** the global setting config.dfoptwgwidth will be automatically changed to the endwidth, if setted.

        suslayer: int, default *20* -- layer # for suspended openings

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width
        * config.dfOpeningOffset: Distance from opening to the center of the opeical waveguide
        * config.dfOpeningWidth:  the width of the opening, perpendicular to the waveguide
        * config.dfOpeningLength: the length of the opening, in parallel with the waveguide
        * config.dfOpeningConnection:  the gap between two openings.
        * config.dfOptRes: control resolution of the curves in micron, recommend and default 0.3

    Example
    -------
        >>>  wg1 = opthedgehog.SuspendOptStraightWaveguide("SuspendOptStraightWaveguide", inports=[(0, 600, 1.0, 0.)], length=400)
    """

    suslayer = 20  # layer # for suspending opening

    def __init__(self, name, inports, length, *, endwidth = -1.0, layer=10, suslayer=20):
        OptStraightWaveguide.__init__(self, name, inports, length, layer, endwidth=endwidth)
        self.suslayer = suslayer
        self.createSuspendingOpening()

    def createSuspendingOpening(self):
        #########################################################
        # change to same _createsuspath function
        shapes = _createsuspath(self.pathnodes, self.suslayer, straight=True)
        self.add(shapes)

        # (x0, y0, dx0, dy0) = self.inports[0]
        # (x1, y1, tmp, tmp) = self.outports[0]
        #
        # xnow = x0
        # ynow = y0
        # lnow = 0.0
        # while lnow < self.length:
        #
        #     yup = y0 + config.dfOpeningOffset
        #     ydown = y0 - config.dfOpeningOffset
        #     xnext = min(xnow + config.dfOpeningLength, xend)
        #     self.add(gdspy.Rectangle((xnow, yup), (xnext, yup + config.dfOpeningWidth), layer=self.suslayer))
        #     self.add(gdspy.Rectangle((xnow, ydown), (xnext, ydown - config.dfOpeningWidth), layer=self.suslayer))
        #     xnow += config.dfOpeningLength + config.dfOpeningConnection

        return None


class SuspendOptBezierConnect(OptBezierConnect):
    """
    OptBezierConnect with openings

    Args:
        name: str
        inports:  List[Tuple[float, float, float, float]]
        shift: Tuple[float, float]
        outputdirection: Tuple[float, float]
        layer: int, default 10
        suslayer: int, default 20

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width
        * config.dfTurningRadius: A reference parameter to generate the Bezier curve.
        * config.dfOpeningOffset: Distance from opening to the center of the opeical waveguide
        * config.dfOpeningWidth:  the width of the opening, perpendicular to the waveguide
        * config.dfOpeningLength: the length of the opening, in parallel with the waveguide
        * config.dfOpeningConnection:  the gap between two openings.
        * config.dfOptRes: control resolution of the curves in micron, recommend and default 0.3


    """

    suslayer = 20
    def __init__(self, name, inports, shift, outputdirection, layer=10, suslayer = 20):
        OptBezierConnect.__init__(self, name, inports, shift, outputdirection, layer=layer)
        self.suslayer = suslayer
        self.createSuspendingOpening()

    def createSuspendingOpening(self):
        #########################################################
        # change to same _createsuspath function
        shapes = _createsuspath(self.pathnodes, self.suslayer)
        self.add(shapes)


class SuspendOptParallelBezierConnect(OptParallelBezierConnect):
    """
        create a suspended Bezier curve optical waveguide
    """
    suslayer = 20

    def __init__(self, name, inport, shift, layer=10, suslayer=20):
        OptParallelBezierConnect.__init__(self, name, inport, shift, layer)
        self.suslayer = suslayer
        self.createSuspendingOpening()

    ### a test code below
    def createSuspendingOpening(self):
        # shiftcell1 = self.copy(self.name+"tmp", exclude_from_current=True, deep_copy = True)
        # shiftcell1 = gdspy.CellReference(shiftcell1, (0, dfOpeningOffset))
        # self.add(shiftcell1)

        #########################################################
        # change to same _createsuspath function
        shapes = _createsuspath(self.pathnodes, self.suslayer)
        self.add(shapes)

        #########################################################
        # OLD version at 0.0.2 below

        # shapes = []
        # connectFlag = True
        # currentLength = 0.0
        # currentNodesPlus = []
        # currentNodesMinus = []
        # (xlast, ylast) = self.pathnodes[0]
        # for (xcurrent, ycurrent) in self.pathnodes[1:]:
        #     currentLength += _pointDist((xlast, ylast), (xcurrent, ycurrent))
        #     dx = xcurrent - xlast
        #     dy = ycurrent - ylast
        #     xlast = xcurrent
        #     ylast = ycurrent
        #     dxn = -dy
        #     dyn = dx
        #     revl = 1.0 / sqrt(float(dxn * dxn + dyn * dyn))
        #     dxn *= revl
        #     dyn *= revl
        #     nodePlus = (xcurrent + dxn * (dfOpeningOffset + dfOpeningWidth / 2.0), ycurrent + dyn * (dfOpeningOffset + dfOpeningWidth / 2.0))
        #     nodeMinus = (xcurrent - dxn * (dfOpeningOffset + dfOpeningWidth / 2.0), ycurrent - dyn * (dfOpeningOffset + dfOpeningWidth / 2.0))
        #     if connectFlag:
        #         if currentLength >= dfOpeningConnection:
        #             connectFlag = not connectFlag
        #             currentLength = 0.0
        #             currentNodesPlus = []
        #             currentNodesMinus = []
        #     else:
        #         currentNodesPlus.append(nodePlus)
        #         currentNodesMinus.append(nodeMinus)
        #         if currentLength >= dfOpeningLength:
        #             shapes.append(gdspy.PolyPath(currentNodesPlus, dfOpeningWidth, layer=self.suslayer))
        #             shapes.append(gdspy.PolyPath(currentNodesMinus, dfOpeningWidth, layer=self.suslayer))
        #             connectFlag = not connectFlag
        #             currentLength = 0.0
        #             currentNodesPlus = []
        #             currentNodesMinus = []
        # if not connectFlag and currentLength > 5.0:
        #     shapes.append(gdspy.PolyPath(currentNodesPlus, dfOpeningWidth, layer=self.suslayer))
        #     shapes.append(gdspy.PolyPath(currentNodesMinus, dfOpeningWidth, layer=self.suslayer))
        #
        # self.add(shapes)

        # NOTES: shift only vertically is WRONG!  Fix on Dec 20, 2018
        # celltmp = gdspy.Cell(self.name+"tmp", exclude_from_current=True)
        # celltmp.add(shapes)
        # shiftplus = dfOpeningOffset + dfOpeningWidth / 2.0
        # shiftminus = - shiftplus
        # self.add(gdspy.CellReference(celltmp, (0, shiftplus)))
        # self.add(gdspy.CellReference(celltmp, (0, shiftminus)))

        return None


class SuspendOptRingCavity(OptRingCavity):
    """
    Circulator ring resonator with Suspended Openings

    Args:
        name: str
        inports: List[Tuple[float, float, float, float]]
        cavityradius:float
        couplinggap:float
        ringwidth: float, default *-1.0* means using the same width as the coupling waveguide,
        layer: int, default 10,
        direction: int, default *1* -- 1 or -1, 1 (-1) indicates the ring is on the left (right) of the waveguide referenced to the input port.
        suslayer: int, default *20* -- layer # for suspended openings

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width
        * config.dfOpeningOffset: Distance from opening to the center of the opeical waveguide
        * config.dfOpeningWidth:  the width of the opening, perpendicular to the waveguide
        * config.dfOpeningLength: the length of the opening, in parallel with the waveguide
        * config.dfOpeningConnection:  the gap between two openings.
        * config.dfOptRes: control resolution of the curves in micron, recommend and default 0.3

    Example:
        >>> cavity2 = opthedgehog.SuspendOptRingCavity("SuspendOptRingCavity", inports=wg5.outports, cavityradius=50.0, couplinggap=2.0, direction=-1, layer = 2, suslayer=20)
    """


    suslayer = 20


    def __init__(self, name, inports, cavityradius, couplinggap, ringwidth=-1.0, layer=10, direction=1, suslayer=20):
        OptRingCavity.__init__(self, name, inports, cavityradius, couplinggap, ringwidth=ringwidth, layer=layer, direction=direction)
        self.suslayer = suslayer
        self.createSuspendingOpening()


    def _getAngPos(self, ang, radius):
        x1 = self.xcenter + np.cos(ang) * radius
        y1 = self.ycenter + np.sin(ang) * radius
        return (x1, y1)


    def createSuspendingOpening(self):
        # add opening for straight waveguide, unter side
        (x0, y0, dx, dy) = self.inports[0]
        (x1, y1, tmp, tmp) = self.outports[0]

        dx, dy = _normalizedxdy(dx, dy)
        nx, ny = -dy, dx

        ltot = sqrt((x1-x0)*(x1-x0)+(y1-y0)*(y1-y0))

        wgopen = []
        for dir in [-1. , 1.]:
            l0 = config.dfOpeningConnection
            offset = config.dfOpeningOffset + config.dfOpeningWidth / 2.
            xl0, yl0 = x0 + dx * l0 + dir * nx * offset, y0 + dy * l0 + ny * offset * dir
            while l0 < ltot:
                l1 = min(l0 + config.dfOpeningLength, ltot)
                xl1, yl1 = x0 + dx * l1 + dir* nx * offset, y0 + dy*l1 + ny * offset * dir
                dist0 = np.sqrt( (self.xcenter - xl1)*(self.xcenter - xl1) + (self.ycenter - yl1) * (self.ycenter - yl1))
                # print(f"{dist0=}   , {self.cavityradius + abs(offset)=}")
                if dist0 >= self.cavityradius + abs(offset):
                    wgopen.append(gdspy.FlexPath([(xl0, yl0), (xl1,yl1)], config.dfOpeningWidth, layer=self.suslayer))
                l0 = l1 + config.dfOpeningConnection
                xl0, yl0 = x0 + dx * l0 + dir * nx * offset, y0 + dy * l0 + ny * offset * dir

        self.add(wgopen)

        # add inner ring openings
        innerRadius = self.cavityradius - config.dfOpeningOffset - 0.5 * config.dfOpeningWidth
        N = int(innerRadius * 2 * 3.14 / config.dfOptRes) + 5

        shapes = []
        connectFlag = True
        currentLength = 0.0
        currentNodes = []
        lastPos = self._getAngPos(0.2, innerRadius)

        for angle in np.arange(0.20, np.pi * 2 + 0.2, 2 * np.pi / N):
            currentPos = self._getAngPos(angle, innerRadius)
            currentLength += _pointDist(lastPos, currentPos)
            lastPos = currentPos

            if connectFlag:
                if currentLength >= config.dfOpeningConnection:
                    connectFlag = not connectFlag
                    currentLength = 0.0
                    currentNodes = []
            else:
                currentNodes.append(currentPos)
                if currentLength >= config.dfOpeningLength:
                    shapes.append(gdspy.PolyPath(currentNodes, config.dfOpeningWidth, layer=self.suslayer))
                    connectFlag = not connectFlag
                    currentLength = 0.0
                    currentNodes = []
        if not connectFlag and len(currentNodes) > 2 and currentLength > config.dfOpeningWidth:
            shapes.append(gdspy.PolyPath(currentNodes, config.dfOpeningWidth, layer=self.suslayer))

        self.add(shapes)

        # add outer ring opening
        outerRadius = self.cavityradius + config.dfOpeningOffset + 0.5 * config.dfOpeningWidth
        N = int(outerRadius * 2 * 3.14 / config.dfOptRes) + 5  # 50nm accuracy for suspended opening

        shapes = []
        connectFlag = True
        currentLength = 0.0
        currentNodes = []
        lastPos = self._getAngPos(0.2, outerRadius)

        for angle in np.arange(0.20, np.pi * 2 + 0.2, 2 * np.pi / N):
            currentPos = self._getAngPos(angle, outerRadius)
            currentLength += _pointDist(lastPos, currentPos)
            lastPos = currentPos

            if connectFlag:
                if currentLength >= config.dfOpeningConnection:
                    connectFlag = not connectFlag
                    currentLength = 0.0
                    currentNodes = []
            else:
                dist0 = np.abs(  (currentPos[1] - y0)*ny + (currentPos[0] - x0)*nx )
                if dist0 > config.dfOpeningOffset + config.dfOpeningWidth / 2.0:
                    currentNodes.append(currentPos)
                if currentLength >= config.dfOpeningLength:
                    if len(currentNodes) > 2:
                        shapes.append(gdspy.PolyPath(currentNodes, config.dfOpeningWidth, layer=self.suslayer))
                    connectFlag = not connectFlag
                    currentLength = 0.0
                    currentNodes = []
        if not connectFlag and len(currentNodes) > 2 and currentLength > config.dfOpeningWidth:
            shapes.append(gdspy.PolyPath(currentNodes, config.dfOpeningWidth, layer=self.suslayer))

        self.add(shapes)
        return None



class SuspendOptRaceTrackCavity(OptRaceTrackCavity):
    """
    Optical Race Track cavity with openings for suspension

    The turning part is using Bezier Path.

    Args:
        name: str
        inports: List[Tuple[float, float, float, float]]
        cavityCornerRadius: float -- The radius for the turing part for the cavity
        cavityLength: float -- The length of the straight part for the cavity.
        cavityWidth: float -- The length of the straight part for the cavity, in direction parallel with the coupling waveguide.
        couplinggap: float -- The gap between the coupling waveguide and the cavity
        ringwidth: float, default *-1.0* indicates same as the coupling waveguide
        layer: int, default *10*
        direction: int, default *1* -- 1 or -1 , the position of the cavity relative to the coupling waveguide
        PlotCouplingWG: bool default *True* -- if *False*, only the cavity is plotted, the coupling waveguide won't be plotted.
        suslayer: int, default *20*

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width
        * config.dfOpeningOffset: Distance from opening to the center of the opeical waveguide
        * config.dfOpeningWidth:  the width of the opening, perpendicular to the waveguide
        * config.dfOpeningLength: the length of the opening, in parallel with the waveguide
        * config.dfOpeningConnection:  the gap between two openings.
        * config.dfOptRes: control resolution of the curves in micron, recommend and default 0.3

    Example:
        >>> cavityR3 = opthedgehog.SuspendOptRaceTrackCavity("SuspendOptRaceTrackCavity", inports=wg6.outports, cavityCornerRadius=50.0, cavityLength=200.0, cavityWidth=0.0, couplinggap=1.0, layer = 2)

    """

    suslayer = 20

    def __init__(self, name: str, inports: List[Tuple[float, float, float, float]],
                 cavityCornerRadius: float, cavityLength: float, cavityWidth: float, couplinggap: float,
                 *, ringwidth=-1.0, layer=10, direction=1, suslayer = 20):
        OptRaceTrackCavity.__init__(self, name, inports=inports, cavityCornerRadius=cavityCornerRadius,
                                    cavityLength=cavityLength, cavityWidth=cavityWidth, couplinggap=couplinggap,
                                    ringwidth=ringwidth, layer = layer, direction=direction)
        self.suslayer = suslayer
        self.createSuspendingOpening()


    def createSuspendingOpening(self):
        #wg opening
        x0, y0, tmp, tmp = self.inports[0]
        x1, y1, tmp, tmp = self.outports[0]

        wgfine = _safepathnodes([(x0, y0), (x1, y1)])
        wgopen = _createsuspath(wgfine, suslayer=self.suslayer, straight=True)
        fatwg = gdspy.FlexPath(wgfine, config.dfOpeningOffset*2)

        cavityfine = _safepathnodes(self.pathnodes)
        cavityopen = _createsuspath(cavityfine, suslayer=self.suslayer)
        cavityfat = gdspy.FlexPath(self.pathnodes, config.dfOpeningOffset*2)

        #boolean all pattern
        merge = gdspy.boolean([*wgopen, *cavityopen], None, "or", max_points=config.MAXPOINTS, layer = self.suslayer)

        merge = gdspy.boolean(merge, fatwg, "not", max_points=config.MAXPOINTS, layer = self.suslayer)
        merge = gdspy.boolean(merge, cavityfat, "not", max_points=config.MAXPOINTS, layer=self.suslayer)
        self.add(merge)


        pass





class SuspendedOptRaceTrackCavityVC(OptRaceTrackCavityVC):
    """

    """
    suslayer = 20
    def __init__(self, name, inport, cavityradius, cavityRacinglength, couplinggap, layer=10, direction=-1, suslayer = 20):
        OptRaceTrackCavityVC.__init__(self, name, inport, cavityradius, cavityRacinglength, couplinggap, layer, direction)
        self.suslayer = suslayer
        self.createSuspendingOpening()

    def createSuspendingOpening(self):
        couplingSuspend = _createsuspath(self.pathnodes, self.suslayer)
        cavitySuspended = _createsuspath(self.pathcavity, self.suslayer)

        #create fab waveguide path to do the boolean operation
        fatwg1 = gdspy.PolyPath(self.pathnodes, width=2*config.dfOpeningOffset, max_points=199, layer=0, corners=1)
        fatwg2 = gdspy.PolyPath(self.pathcavity, width=2 * config.dfOpeningOffset, max_points=199, layer=0, corners=1)
        fatwgTot = gdspy.fast_boolean(fatwg1, fatwg2, "or", precision= 0.01)
        #
        couplingSuspend = gdspy.fast_boolean(couplingSuspend,fatwgTot, "not", layer = self.suslayer, precision= 0.01)
        cavitySuspended = gdspy.fast_boolean(cavitySuspended,fatwgTot, "not", layer = self.suslayer, precision= 0.01)

        self.add(couplingSuspend)
        self.add(cavitySuspended)

        pass




class SuspendOptYsplitter(OptYsplitter):
    suslayer = 20
    def __init__(self, name, inports, splitshift, layer=10, suslayer=20):
        OptYsplitter.__init__(self, name, inports, splitshift, layer = layer)
        self.suslayer = suslayer
        self.createSuspendingOpening()

    def createSuspendingOpening(self):

        SuspendedPath1 = _createsuspath(self.pathnodes1, self.suslayer, reverseflag= False)
        SuspendedPath2 = _createsuspath(self.pathnodes2, self.suslayer, reverseflag= False)

        #create fab waveguide path to do the boolean operation
        fatwg1 = gdspy.PolyPath(self.pathnodes1, width=2*config.dfOpeningOffset, max_points=config.MAXPOINTS, layer=0, corners=1)
        fatwg2 = gdspy.PolyPath(self.pathnodes2, width=2 * config.dfOpeningOffset, max_points=config.MAXPOINTS, layer=0, corners=1)
        fatwgTot = gdspy.boolean(fatwg1, fatwg2, "or", precision= 0.01, max_points=config.MAXPOINTS)
        #
        SuspendedPath1 = gdspy.fast_boolean(SuspendedPath1,fatwgTot, "not", layer = self.suslayer, precision= 0.01, max_points=config.MAXPOINTS)
        SuspendedPath2 = gdspy.fast_boolean(SuspendedPath2,fatwgTot, "not", layer = self.suslayer, precision= 0.01, max_points=config.MAXPOINTS)
        SuspendedPathT = gdspy.fast_boolean(SuspendedPath1, SuspendedPath2, "or", layer=self.suslayer, precision=0.01, max_points=config.MAXPOINTS)

        # self.add(SuspendedPath1)
        self.add(SuspendedPathT)
        # shapes = []
        # # upper bound opening
        # connectFlag = True
        # currentLength = 0.0
        # currentNodesPlus = []
        # currentNodesMinus = []
        # (xlast, ylast) = self.pathnodes2[0]
        # for (xcurrent, ycurrent) in self.pathnodes2[1:]:
        #     currentLength += _pointDist((xlast, ylast), (xcurrent, ycurrent))
        #     dx = xcurrent - xlast
        #     dy = ycurrent - ylast
        #     xlast = xcurrent
        #     ylast = ycurrent
        #     dxn = -dy
        #     dyn = dx
        #     revl = 1.0 / sqrt(float(dxn * dxn + dyn * dyn))
        #     dxn *= revl
        #     dyn *= revl
        #     nodePlus = (xcurrent + dxn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0), ycurrent + dyn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0))
        #     nodeMinus = (xcurrent - dxn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0), ycurrent - dyn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0))
        #     if connectFlag:
        #         if currentLength >= config.dfOpeningConnection:
        #             connectFlag = not connectFlag
        #             currentLength = 0.0
        #             currentNodesPlus = []
        #             currentNodesMinus = []
        #     else:
        #         currentNodesPlus.append(nodePlus)
        #         if ycurrent - dyn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0) > self.inports[0][1]:
        #             currentNodesMinus.append(nodeMinus)
        #         if currentLength >= config.dfOpeningLength:
        #             shapes.append(gdspy.PolyPath(currentNodesPlus, config.dfOpeningWidth, layer=self.suslayer))
        #             if len(currentNodesMinus) > 10:  # make sure one opening is long engough .. sech point is about 0.06 um. so it's about 5 um
        #                 shapes.append(gdspy.PolyPath(currentNodesMinus, config.dfOpeningWidth, layer=self.suslayer))
        #             connectFlag = not connectFlag
        #             currentLength = 0.0
        #             currentNodesPlus = []
        #             currentNodesMinus = []
        # if not connectFlag and currentLength > 5.0:
        #     shapes.append(gdspy.PolyPath(currentNodesPlus, config.dfOpeningWidth, layer=self.suslayer))
        #     if len(currentNodesMinus) > 10:
        #         shapes.append(gdspy.PolyPath(currentNodesMinus, config.dfOpeningWidth, layer=self.suslayer))
        #
        # # lower opening of second out port
        # connectFlag = True
        # currentLength = 0.0
        # currentNodesPlus = []
        # currentNodesMinus = []
        # (xlast, ylast) = self.pathnodes1[0]
        # for (xcurrent, ycurrent) in self.pathnodes1[1:]:
        #     currentLength += _pointDist((xlast, ylast), (xcurrent, ycurrent))
        #     dx = xcurrent - xlast
        #     dy = ycurrent - ylast
        #     xlast = xcurrent
        #     ylast = ycurrent
        #     dxn = -dy
        #     dyn = dx
        #     revl = 1.0 / sqrt(float(dxn * dxn + dyn * dyn))
        #     dxn *= revl
        #     dyn *= revl
        #     nodePlus = (xcurrent + dxn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0), ycurrent + dyn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0))
        #     nodeMinus = (xcurrent - dxn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0), ycurrent - dyn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0))
        #     if connectFlag:
        #         if currentLength >= config.dfOpeningConnection:
        #             connectFlag = not connectFlag
        #             currentLength = 0.0
        #             currentNodesPlus = []
        #             currentNodesMinus = []
        #     else:
        #         if ycurrent + dyn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0) < self.inports[0][1]:  # check if it conflicts with another waveguide
        #             currentNodesPlus.append(nodePlus)
        #         currentNodesMinus.append(nodeMinus)
        #         if currentLength >= config.dfOpeningLength:
        #             if len(currentNodesPlus) > 10:
        #                 shapes.append(gdspy.PolyPath(currentNodesPlus, config.dfOpeningWidth, layer=self.suslayer))
        #             shapes.append(gdspy.PolyPath(currentNodesMinus, config.dfOpeningWidth, layer=self.suslayer))
        #             connectFlag = not connectFlag
        #             currentLength = 0.0
        #             currentNodesPlus = []
        #             currentNodesMinus = []
        # if not connectFlag and currentLength > 5.0:
        #     if len(currentNodesPlus) > 10:
        #         shapes.append(gdspy.PolyPath(currentNodesPlus, config.dfOpeningWidth, layer=self.suslayer))
        #     shapes.append(gdspy.PolyPath(currentNodesMinus, config.dfOpeningWidth, layer=self.suslayer))
        #
        # # bool OR all shape to avoid overlay
        # shapes = gdspy.fast_boolean(shapes, None, "or", layer=self.suslayer)
        # self.add(shapes)
        # return None


class SuspendOptYmerger(OptYmerger):
    suslayer = 20
    def __init__(self, name, inports, splitshift: float, layer=10, suslayer=20):
        OptYmerger.__init__(self, name, inports, splitshift, layer=layer)
        self.suslayer = suslayer
        self.createSuspendingOpening()

    def createSuspendingOpening(self):

        #updated opening for Y merger, using boolean method

        reverse1 = list(self.pathnodes1)
        #reverse1.reverse()  chenged due to updated OptYmerger
        reverse2 = list(self.pathnodes2)
        #reverse2.reverse()  chenged due to updated OptYmerger
        SuspendedPath1 = _createsuspath(reverse1, self.suslayer, reverseflag= False)
        SuspendedPath2 = _createsuspath(reverse2, self.suslayer, reverseflag= False)

        #create fab waveguide path to do the boolean operation
        fatwg1 = gdspy.PolyPath(self.pathnodes1, width=2*config.dfOpeningOffset, max_points=config.MAXPOINTS, layer=0, corners=1)
        fatwg2 = gdspy.PolyPath(self.pathnodes2, width=2 * config.dfOpeningOffset, max_points=config.MAXPOINTS, layer=0, corners=1)
        fatwgTot = gdspy.boolean(fatwg1, fatwg2, "or",  max_points=config.MAXPOINTS)
        #
        SuspendedPath1 = gdspy.fast_boolean(SuspendedPath1,fatwgTot, "not", layer = self.suslayer, max_points=config.MAXPOINTS)
        SuspendedPath2 = gdspy.fast_boolean(SuspendedPath2,fatwgTot, "not", layer = self.suslayer,  max_points=config.MAXPOINTS)
        SuspendedPathT = gdspy.fast_boolean(SuspendedPath1, SuspendedPath2, "or", layer=self.suslayer,  max_points=config.MAXPOINTS)

        # self.add(SuspendedPath1)
        self.add(SuspendedPathT)

        return None


def _createsuspath(path, suslayer, reverseflag = False, straight=False):

    shapes = []
    if reverseflag:   # the reverseflag dealing with the correct link unit
        connectFlag = False
        (xlast, ylast) = path[-1]
        currentLength = 0.0
        i = -2
        while currentLength < config.dfOpeningConnection:
            (xcurrent, ycurrent) = path[i]
            i -= 1
            currentLength += _pointDist((xlast, ylast), (xcurrent, ycurrent))
            xlast = xcurrent
            ylast = ycurrent
        Lend = len(path) + i + 1
    else:
        connectFlag = True
        Lend = len(path)

    currentLength = config.dfOpeningConnection/2.
    currentNodesPlus = []
    currentNodesMinus = []
    (xlast, ylast) = path[0]
    for (xcurrent, ycurrent) in path[1:Lend]:    #added skip path to reduce resolution, --> fast and small file sizes
        currentLength += _pointDist((xlast, ylast), (xcurrent, ycurrent))
        dx = xcurrent - xlast
        dy = ycurrent - ylast
        xlast = xcurrent
        ylast = ycurrent
        dxn = -dy
        dyn = dx
        if float(dxn * dxn + dyn * dyn)< 1e-8:   # skip repeated points
            continue
        revl = 1.0 / sqrt(float(dxn * dxn + dyn * dyn))
        dxn *= revl
        dyn *= revl
        nodePlus = (xcurrent + dxn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0), ycurrent + dyn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0))
        nodeMinus = (xcurrent - dxn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0), ycurrent - dyn * (config.dfOpeningOffset + config.dfOpeningWidth / 2.0))
        if connectFlag:
            if currentLength >= config.dfOpeningConnection:
                connectFlag = not connectFlag
                currentLength = 0.0
                currentNodesPlus = []
                currentNodesMinus = []
        else:
            currentNodesPlus.append(nodePlus)
            currentNodesMinus.append(nodeMinus)
            if currentLength >= config.dfOpeningLength:
                if straight:
                    shapes.append(gdspy.PolyPath([currentNodesPlus[0],currentNodesPlus[-1]], config.dfOpeningWidth, layer=suslayer))
                    shapes.append(gdspy.PolyPath([currentNodesMinus[0],currentNodesMinus[-1]], config.dfOpeningWidth, layer=suslayer))
                else:
                    shapes.append(gdspy.PolyPath(currentNodesPlus, config.dfOpeningWidth, layer=suslayer))
                    shapes.append(gdspy.PolyPath(currentNodesMinus, config.dfOpeningWidth, layer=suslayer))
                connectFlag = not connectFlag
                currentLength = 0.0
                currentNodesPlus = []
                currentNodesMinus = []

    if not connectFlag and currentLength > 1.0:
        if straight:
            shapes.append(gdspy.PolyPath([currentNodesPlus[0], currentNodesPlus[-1]], config.dfOpeningWidth, layer=suslayer))
            shapes.append(gdspy.PolyPath([currentNodesMinus[0], currentNodesMinus[-1]], config.dfOpeningWidth, layer=suslayer))
        else:
            shapes.append(gdspy.PolyPath(currentNodesPlus, config.dfOpeningWidth, layer=suslayer))
            shapes.append(gdspy.PolyPath(currentNodesMinus, config.dfOpeningWidth, layer=suslayer))

    return shapes


#################################################  The following calss are rebuilt for SBS proejcts

class SuspendOptStraightWaveguideAdvanced(OptStraightWaveguide):
    """
        SuspendOptStraightWaveguideAdvanced
    """

    suslayer = 20
    susOffset = -1.0
    susSeg = -1.0
    susCon = 1.0
    susWidth = -1.0

    _dx, _dy = 0.0, 0.0

    def __init__(self, name, inports, length, optlayer = 10, suslayer=20, *, susSeg = -1.0, susOffset=-1.0, susCon = -1.0, susWidth=-1.0):
        OptStraightWaveguide.__init__(self, name, inports, length = length, layer = optlayer)
        #dx, dy already normalized in super class

        self.suslayer = suslayer

        if susSeg > 0.0:
            self.susSeg = susSeg
        else:
            self.susSeg = config.dfOpeningLength

        if susOffset > 0.0:
            self.susOffset = susOffset
        else:
            self.susOffset = config.dfOpeningOffset

        if susCon > 0.0:
            self.susCon = susCon
        else:
            self.susCon = config.dfOpeningConnection

        if susWidth > 0.0:
            self.susWidth = susWidth
        else:
            self.susWidth = config.dfOpeningWidth

        tmp, tmp, self._dx, self._dy = self.inports[0]

        self.createMask()


    def createMask(self):
        xs, ys, dx, dy = self.inports[0]
        nx, ny = dy, -dx

        for alpha in [-1.0, 1.0]:
            x1, y1 = xs + alpha * nx * (self.susOffset + 0.5*self.susWidth), ys + alpha * ny * (self.susOffset + 0.5*self.susWidth)

            flag = True
            while flag:
                x2, y2, flag = self._safestep(x1, y1, self.susSeg)
                seg = gdspy.FlexPath([(x1,y1),(x2,y2)], self.susWidth, layer = self.suslayer)
                self.add(seg)
                x1, y1, flag = self._safestep(x2, y2, self.susCon)
        pass


    def _safestep(self, x, y, step):
        x1, y1, dx, dy = self.inports[0]
        x2, y2, tmp, tmp = self.outports[0]

        l = sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))

        xs, ys = x + step * dx, y + step*dy
        l2 = (xs-x1)*dx + (ys-y1)*dy
        if l2 <= l:   # good
            return xs, ys, True
        else:         # cut off
            lorigin = (x-x1)*dx + (y - y1)* dy
            if lorigin < l:
                shiftx, shifty = (l-lorigin) * dx , (l-lorigin) * dy
                return x+shiftx, y+shifty, False
            else:
                return x, y, False
        pass


def _safepathnodes(points: List[Tuple[float, float]]):
    res = []
    xlast, ylast = 0, 0
    if len(points) > 0:
        res.append(points[0])
        xlast, ylast = points[0]
    else:
        return res

    for x, y in points[1:]:
        dist = _pointDist((x,y), (xlast, ylast))
        if dist < config.dfOptRes*3:    #good
            res.append((x, y))
        else:
            #add more points
            N = int(dist / (config.dfOptRes) + 2)
            for i in range(N):
                xi = xlast * float(N-i) / N + x * float(i) / N
                yi = ylast * float(N - i) / N + y * float(i) / N
                res.append((xi,yi))
            res.append((x,y))
        xlast, ylast = x, y

    return res

######################################################################################
##  opthedgehog ---
##   A Python package for integreated optices.
##  Developed by: Linbo Shao
##
##  Description:
##     This files contains classes to generate optical components with positive resist
##     Initially Design for Raytheon - Loncar project
##  Data:
##     July 31, 2019
######################################################################################


from math import sqrt
from .optCells import *
from .optCells import _normalizedxdy
from gdspy import Cell
import numpy as np

from . import config

class PosOptStraightWaveguide(OptCell):
    """
        straight wave guide defined by grooves -- for positive resisit
    """
    etchlayer = 15
    flagKeep = False

    def __init__(self, name, inports, length, *, layer=10, etchlayer=15, keepFirst = False):
        OptCell.__init__(self, name, layer)
        if isinstance(inports, list):
            self.inports = inports
        else:
            self.inports.append(inports)

        self.flagKeep = keepFirst

        self.etchlayer = etchlayer
        self.length = length
        (x, y, dx, dy) = self.inports[0]

        if dx * dx + dy * dy < 0.1:
            raise Exception("[opthedgehog] Value error", "undefined waveguide direction at (%f,%f, %f,%f)" % (x, y, dx, dy))

        norm = np.sqrt(dx * dx + dy * dy)
        dx = dx / norm
        dy = dy / norm
        self.inports = [(x, y, dx, dy)]  # normailized the input direction

        xend = x + dx * length
        yend = y + dy * length

        self.outports = [(xend, yend, dx, dy)]

        self.createEtchingMask()

    def createEtchingMask(self):
        """
        create mask
        :return: none
        """
        (x0,y0,dx,dy)  = self.inports[0]
        (xend, yend, dxend, dyend) = self.outports[0]

        if self.flagKeep:
            self.add(gdspy.FlexPath([(x0,y0),(xend,yend)], config.dfoptwgwidth, layer = self.layer )  )

        self.add(_createEtchPath([(x0,y0),(xend,yend)], etchlayer=self.etchlayer))

        return None


class PosOptBezierConnect(OptBezierConnect):
    """

    """
    etchlayer = 15
    flagKeep = False

    def __init__(self, name, inports, shift, outputdirection, *, layer=10, etchlayer=15, keepFirst = False):
        OptBezierConnect.__init__(self, name, inports, shift, outputdirection, layer=layer)
        self.etchlayer = etchlayer

        self.flagKeep = keepFirst

        self.createEtchMask()

    def createEtchMask(self):
        """
        create mask for positive waveguide
        :return:
        """
        #remove oroginal path
        if not self.flagKeep:
            self.remove_paths(lambda a:True)
            self.remove_polygons(lambda a,layer,c: layer == self.layer)

        self.add(_createEtchPath(self.pathnodes, etchlayer=self.etchlayer))

        pass


class PosOptBezierWaveguide(OptBezierWaveguide):
    """

    """
    etchlayer = 15
    flagKeep = False


    def __init__(self, name: str,
                 inports: List[Tuple[float, float, float, float]],
                 controlpoints: List[Tuple[float, float]],  # relative control points for Bezier curve, the inport is added automatically
                 *,
                 layer = 10,
                 etchlayer = 15,
                 keepFirst = False):
        super().__init__(name, inports, controlpoints, layer = layer)
        self.etchlayer = etchlayer
        self.flagKeep = keepFirst
        self.createEtchMask()

    def createEtchMask(self):
        if not self.flagKeep:
            self.remove_paths(lambda a:True)
            self.remove_polygons(lambda a,layer,c: layer == self.layer)

        self.add(_createEtchPath(self.pathnodes, etchlayer=self.etchlayer))
        pass


class PosOptYsplitter(OptYsplitter):
    """

    """
    etchlayer = 15
    flagKeep = False

    def __init__(self, name, inports: List[Tuple[float, float, float, float]], splitshift: Tuple[float, float],
                 *, layer=10, etchlayer = 15, keepFirst = False):
        super().__init__(name, inports, splitshift, layer=layer)
        self.etchlayer = etchlayer
        self.flagKeep = keepFirst
        self.createEtchMask()

    def createEtchMask(self):

        wgpatten = []
        polys = self.get_polygons(by_spec=True)
        for layer, dataset in polys:
            if layer == self.layer:
                wgpatten.extend(polys[(layer, dataset)])

        etch1 = _createEtchPath(self.pathnodes1, etchlayer=self.etchlayer)
        etch2 = _createEtchPath(self.pathnodes2, etchlayer=self.etchlayer)

        etchwg = [path.to_polygonset() for path in etch1+etch2 ]

        etchmerge = gdspy.boolean(etchwg, wgpatten, "not", max_points=config.MAXPOINTS, layer=self.etchlayer)

        self.add(etchmerge)

        if not self.flagKeep:
            self.remove_paths(lambda a:True)
            self.remove_polygons(lambda a,layer,c: layer == self.layer)

        pass




class PosOpt2x2MMI(Opt2x2MMI):
    """

    """
    etchlayer = 15

    def __init__(self, name, inports, endwgwidth, MMIwidth, MMIlength, MMIinputoffset, layer=10, etchlayer = 15):
        Opt2x2MMI.__init__(self, name, inports, endwgwidth, MMIwidth, MMIlength, MMIinputoffset, layer)
        self.etchlayer = etchlayer

        self.createEtchMask()

    def createEtchMask(self):
        """
        create mask for positive resist
        :return:
        """
        path1 = _createEtchPath(self.pathnodes1, etchlayer=self.etchlayer)
        path2 = _createEtchPath(self.pathnodes2, etchlayer=self.etchlayer)
        path3 = _createEtchPath(self.pathnodes3, etchlayer=self.etchlayer)
        path4 = _createEtchPath(self.pathnodes4, etchlayer=self.etchlayer)

        ### MMI mask
        x0 = self.MMIstartx
        y0 = self.MMIy
        length = self.MMIlength + 20.0
        MMImask = gdspy.PolyPath( [(x0 , y0), (x0+length, y0)], width = self.MMIwidth + 2.0*config.dfPosOptCellOpening, layer = self.etchlayer )

        ###  merge all etch part
        shapes = []
        shapes.extend(path1)
        shapes.extend(path2)
        shapes.extend(path3)
        shapes.extend(path4)
        shapes.append(MMImask)
        mergedmask = gdspy.fast_boolean(shapes, None,"or",layer = self.etchlayer)

        finalmask = gdspy.boolean(mergedmask, self.get_polygons(), "not", layer = self.etchlayer)

        self.remove_paths(lambda a: True)
        self.remove_polygons(lambda a, layer, c: layer == self.layer)

        self.add(finalmask)


class PosOptTaper(OptCell):
    """
       Taper Waveguide for positive resisit
    """
    length = 1.0
    startwidth = 0.0
    endwidth = 0.0
    alpha = 1.0
    keepfirst = False

    def __init__(self, name, inports, length, startwidth, endwidth, alpha=1.0, etchlayer=15, layer = 10,keepFirst=False):
        OptCell.__init__(self, name, layer = layer)
        if isinstance(inports, list):
            self.inports = inports
        else:
            self.inports.append(inports)

        self.length = length
        self.startwidth = startwidth
        self.endwidth = endwidth
        self.alpha = alpha
        self.etchlayer = etchlayer
        self.keepfirst = keepFirst

        (x, y, dx, dy) = self.inports[0]

        if dx * dx + dy * dy < 0.1:
            raise Exception("[opthedgehog] Value error", "undefined waveguide direction at (%f,%f, %f,%f)" % (x, y, dx, dy))

        norm = np.sqrt(dx * dx + dy * dy)
        dx = dx / norm
        dy = dy / norm
        self.inports = [(x, y, dx, dy)]  # normailized the input direction

        xend = x + dx * length
        yend = y + dy * length

        self.outports = [(xend, yend, dx, dy)]
        self.createEtchMask()

    def createEtchMask(self):
        """

        :return:
        """

        #always from small end to large end
        if self.startwidth<=self.endwidth:
            (x0, y0, dx, dy) = self.inports[0]
            (xend, yend, tmp, tmp) = self.outports[0]
            w0 = self.startwidth
            wend = self.endwidth
        else:
            (x0, y0, dx, dy) = self.outports[0]
            (xend, yend, tmp, tmp) = self.inports[0]
            dx = -dx
            dy = -dy
            w0 = self.endwidth
            wend = self.startwidth

        dxn = dy
        dyn = -dx

        upperSlot = []
        lowerSlot = []
        wgup = []
        wgdown = []

        N = int(self.length/config.dfOptRes + 5)

        for i in range(-1,N+2):

            #fix the edge of the slot
            j = i
            if i < 0:
                j = 0
            if i >N :
                j = N

            z = (float(i)/float(N))*(self.length - config.dfPosOptCellOpening)
            if i > N:
                z = self.length
            widthcurrent = w0 + (wend - w0) * ((float(j) / float(N)) ** self.alpha)

            #upperpoint
            xcurrent = x0 + dx * z + dxn * 0.5 * (widthcurrent + config.dfPosOptCellOpening)
            ycurrent = y0 + dy * z + dyn * 0.5 * (widthcurrent + config.dfPosOptCellOpening)
            upperSlot.append((xcurrent, ycurrent))

            xcurrent = x0 + dx * z - dxn * 0.5 * (widthcurrent + config.dfPosOptCellOpening)
            ycurrent = y0 + dy * z - dyn * 0.5 * (widthcurrent + config.dfPosOptCellOpening)
            lowerSlot.append((xcurrent, ycurrent))

            xcup = x0 + dx * z + dxn * 0.5 * (widthcurrent)
            ycup = y0 + dy * z + dyn * 0.5 * (widthcurrent)
            wgup.append((xcup, ycup))
            xcdown = x0 + dx * z - dxn * 0.5 * (widthcurrent)
            ycdown = y0 + dy * z - dyn * 0.5 * (widthcurrent)
            wgdown.append((xcdown, ycdown))

        self.add(gdspy.FlexPath(upperSlot, width = config.dfPosOptCellOpening, layer = self.etchlayer, max_points=config.MAXPOINTS))
        self.add(gdspy.FlexPath(lowerSlot, width=config.dfPosOptCellOpening, layer=self.etchlayer, max_points=config.MAXPOINTS))

        if self.keepfirst:
            wgdown.reverse()
            self.add(gdspy.Polygon([*wgup, *wgdown], layer=self.layer))

        return None


class PosOptEllipseLens(Cell):
    a = 10.0
    b = 10.0
    c = 10.0
    ep = 10.0
    f = 10.0
    fpos = (0,0)
    width = 10.0
    direction  = 1
    etchlayer = 15
    def __init__(self,name, flens, ep, width, focuspos = (0,0), direction = 1, etchlayer = 15):
        name0 = name + "_%d" % (config._index())
        Cell.__init__(self,name0)
        self.f = flens
        self.ep = ep
        self.a = flens / (1.00+ep)
        self.c = self.a * self.ep
        self.b = sqrt(self.a*self.a - self.c*self.c )
        self.width = width
        self.fpos = focuspos
        self.direction = direction
        self.etchlayer = etchlayer

        print("[OptHedgehog] EllipseLens generation -- focal length = %.3f, e = %.3f, a = %.3f, b = %.3f, c = %.3f, focusspot = %s, direction =%d"%
              (self.f, self.ep, self.a, self.b, self.c, str(self.fpos), self.direction))

        self.createEtchMask()

    def createEtchMask(self):
        ymin =  - min(self.width/2, self.b)
        ymax = -ymin
        segN = int((ymax - ymin)/0.010 + 5)
        ylist = np.linspace(ymin, ymax, segN)
        poslist = []
        for y in ylist:
            x = self.direction*( self.a*sqrt(1.00 - y*y / (self.b*self.b)))
            poslist.append((x,y))

        linex = self.a*self.a / self.c *self.direction
        poslist.append((linex, ymax))
        poslist.append((linex, ymin))

        pattern = gdspy.Polygon(poslist,layer = self.etchlayer)
        self.add(pattern.fracture())

        refcirc = gdspy.Round((-self.c,0), radius =  1.0, layer = 11)
        self.add(refcirc)

        pass



class PosOptAddOnWaveguideCoupler(OptAddOnWaveguideCoupler):
    """

    """
    etchlayer = 15

    flagKeep = False
    refPatterns = None
    reflayer:List[int] = None

    def __init__(self, name: str,
                 inports: List[Tuple[float, float, float, float]],
                 couplingPos: List[Tuple[float, float, float, float]],
                 couplingLength: float,  # the length of coupling region
                 couplingPitch: float,
                 *,
                 layer=10,
                 curveParameter: float = -1.,
                 etchlayer = 15,
                 keepFirst = False,
                 refPattern: List[gdspy.Cell] = None,
                 reflayer: List[int] = None
                 ):
        super().__init__(name, inports, couplingPos,
                 couplingLength,
                 couplingPitch,
                 layer = layer,
                 curveParameter = curveParameter)


        self.etchlayer = etchlayer

        self.flagKeep = keepFirst
        self.refPatterns = refPattern
        self.reflayer = reflayer
        if self.reflayer is None:
            self.reflayer = [layer, etchlayer]

        self.createEtchMask()
        pass

    def createEtchMask(self):


        etchwg1 = _createEtchPath(self.pathnodes, etchlayer=self.etchlayer)

        #convert to polygen
        etchwg1poly = [ path.to_polygonset() for path in etchwg1]

        #get the polygon from the ref cell
        if self.refPatterns is not None:
            selectpolys = []

            for r in self.refPatterns:
                polys = r.get_polygons(by_spec=True)
                for layer,dataset in polys:
                    if layer in self.reflayer:
                        selectpolys.extend(polys[(layer, dataset)])

            #perform boolean
            etchwg1 = gdspy.boolean(etchwg1poly, selectpolys, "not", max_points=config.MAXPOINTS, layer=self.etchlayer)

        self.add(etchwg1)


        #getcurrent path
        current = None
        c = self.get_polygons(by_spec=True)
        if (self.layer, 0) in c:
            current = c[(self.layer, 0)]


        #modify the other patterns
        if self.refPatterns is not None:
            for r in self.refPatterns:
                polys = r.get_polygons(by_spec=True)
                modifypolys = []
                for layer, dataset in polys:
                    if layer == self.etchlayer:
                        modifypolys.extend(polys[(layer, dataset)])

                r.remove_polygons( lambda  pts, layer, datatype: layer == self.etchlayer)
                r.remove_paths(lambda p:  self.etchlayer in p.layers)

                modifypolys = gdspy.boolean(modifypolys, current, "not", max_points=config.MAXPOINTS, layer = self.etchlayer)
                r.add(modifypolys)
        pass



    #end of PosOptAddOnWaveguideCoupler


class PosOptDiskCavity(OptDiskCavity):
    """
    Circulator Disk resonator for using Positive Resist

    Args:
        name: str
        inports: List[Tuple[float, float, float, float]]
        cavityradius:float
        couplinggap:float
        layer: int, default 10,
        etchlayer: int, default 15,
        direction: int, default *1* -- 1 or -1, 1 (-1) indicates the ring is on the left (right) of the waveguide referenced to the input port.
        PlotCouplingWG: bool default *True* -- if *False*, the coupling waveguide won't be plotted.
        refPattern: bool default *False* -- if *True*, the pattern for the original negative pattern will be kept.
        openingPattern: float, default -1 -- if > 0 , an additional layer will added, extend the the disk radius.
        openinglayer: int, default 16 -- layer for the additional layer

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width
        * config.dfPosOptCellOpening:  Width of the opening etch

    Example:
        >>> opthedgehog.PosOptDiskCavity("OptDiskCavity", inports=wg1.outports, cavityradius=50.0, couplinggap=2.0, direction=1, layer=2,openingPattern = 5.)

    """
    etchlayer = 15
    openinglayer = 16
    refPattern = True
    openingPattern = -1.

    def __init__(self, name: str, inports: List[Tuple[float, float, float, float]],
                 cavityradius: float, couplinggap: float,
                 *, layer: int = 10, etchlayer=15,  direction: int = 1,
                 PlotCouplingWG: bool = True, refPattern: bool = False,
                 openingPattern : float = -1., openinglayer: int = 16):
        OptDiskCavity.__init__(self, name, inports, cavityradius=cavityradius, couplinggap=couplinggap,
                               layer = layer, direction = direction, PlotCouplingWG = PlotCouplingWG)

        self.etchlayer = etchlayer
        self.refPattern = refPattern
        self.openingPattern = openingPattern
        self.openinglayer = openinglayer
        self.createEtchMask()

    def createEtchMask(self):

        # waveguide opening etch
        startpos = ( self.inports[0][0], self.inports[0][1] )
        endpos = ( self.outports[0][0], self.outports[0][1] )
        wgetch = _createEtchPath( [startpos, endpos], etchlayer=self.etchlayer)
        wgetch = [path.to_polygonset() for path in wgetch]


        # disk opening etch
        disketch = gdspy.Round(
            center = (self.xcenter, self.ycenter),
            radius= self.cavityradius + config.dfPosOptCellOpening,
            layer = self.etchlayer,
            max_points=config.MAXPOINTS
        )

        #boolean operation

        etchmerge = gdspy.boolean([*wgetch, disketch], None, "or", layer=1, max_points=config.MAXPOINTS)
        # self.add(etchmerge)

        #boolean
        r = self.get_polygons(by_spec=True)
        optpat = None
        if (self.layer, 0) in r:
            optpat = r[(self.layer, 0)]

        etchpattern = gdspy.boolean(etchmerge, optpat, "not", layer=self.etchlayer, max_points=config.MAXPOINTS)
        self.add(etchpattern)

        #delete the original pattern
        if not self.refPattern:
            self.remove_polygons(lambda pts, layer, datatype: layer == self.layer)
            self.remove_paths(lambda p: self.layer in p.layers)

        #add pattern for opening
        if self.openingPattern > 0.:
            openp = gdspy.Round(
                        center = (self.xcenter, self.ycenter),
                        radius= self.cavityradius + self.openingPattern,
                        layer = self.openinglayer,
                        max_points=config.MAXPOINTS
                    )
            self.add(openp)

        pass


class PosOptCurvedGratingCoupler(OptCell):

    # direction of the grating coupling
    reverse = False

    # grating parameters
    gN: int = 0
    gPeriod = 1.0
    gDuty = 1.0
    gWidth = 0.0

    # tapering
    rext = 0.0
    tapRadius = 0.0
    tapLen = 0.0
    tapEndwidth = 0.0

    # internal cariables
    _dx = 0.0
    _dy = 0.0
    _nx = 0.0
    _ny = 0.0

    #Pos cell
    openinglayer = 16
    keepFirst = False

    def __init__(self, name: str,
                 inports: List[Tuple[float, float, float, float]],
                 gratingN: int,
                 gratingPeroid: float,
                 reverse=False,
                 *,
                 focusRadius=20.0,  # the Radius of focusing waveguide
                 gratingWidth=13.0,
                 gratingDuty: float = 0.5,
                 layer=10,
                 etchlayer: int = 15,
                 keepFirst: bool = True,
                 ):
        OptCell.__init__(self, name=name, layer=layer)

        self.inports = inports
        (x0, y0, dx, dy) = self.inports[0]
        dx, dy = _normalizedxdy(dx, dy)  # propogation direction
        self._dx = dx
        self._dy = dy

        self.reverse = reverse

        self.gN = gratingN
        self.gPeriod = gratingPeroid
        self.gDuty = gratingDuty

        self.gWidth = gratingWidth

        self.tapRadius = focusRadius
        self.tapEndwidth = config.dfoptwgwidth

        self.openinglayer = etchlayer
        self.keepFirst = keepFirst

        # calculate tap lens
        w1 = gratingWidth
        r1 = focusRadius
        w0 = self.tapEndwidth
        r0 = w0 * r1 / w1
        #   w1        w0
        #  ----- == ------
        #   r1        r0
        self.rext = r0
        self.tapLen = focusRadius - r0

        # calculate outports
        xend, yend = self._step(x0, y0, self.gPeriod * self.gN + self.tapLen)
        self.outports = [(xend, yend, dx, dy)]

        # mask
        self.createMask()
        # outports not generated here.

    def createMask(self):
        if self.reverse:
            (x0, y0, dx, dy) = self.inports[0]
            x0, y0 = self._step(x0, y0, -self.rext)

        else:
            (x0, y0, dx, dy) = self.outports[0]
            x0, y0 = self._step(x0, y0, self.rext)
            dx, dy = -dx, -dy

        dx, dy = _normalizedxdy(dx, dy)  # propogation direction
        nx, ny = dy, -dx  # normal vector
        self._dx = dx
        self._dy = dy
        self._nx = nx
        self._ny = ny

        patterns = []

        dirRad = np.arctan2(dy, dx)

        # taper waveguide
        wcur = self.gWidth
        rcur = self.tapRadius

        diffang = np.arctan2(wcur / 2.0, rcur)

        circle = gdspy.Round((x0, y0), self.tapRadius,
                             initial_angle=dirRad - diffang, final_angle=dirRad + diffang,
                             max_points=config.MAXPOINTS,
                             )

        #posExtent
        posdist = config.dfPosOptCellOpening/np.tan(diffang)
        xpos, ypos = self._step(x0, y0, - posdist)
        # posExtAng = np.arctan2(wcur / 2.0 + config.dfPosOptCellOpening, rcur)
        Poscircle = gdspy.Round((xpos, ypos), self.tapRadius + posdist - 1.5,
                             initial_angle=dirRad - diffang, final_angle=dirRad + diffang,
                             max_points=config.MAXPOINTS,
                             )

        xc1, yc1 = self._step(x0, y0, self.rext - 0.001)
        xup, yup = xc1 + nx * (self.tapEndwidth + config.dfPosOptCellOpening), yc1 + ny * (self.tapEndwidth + config.dfPosOptCellOpening)
        xdown, ydown = xc1 - nx * (self.tapEndwidth + config.dfPosOptCellOpening), yc1 - ny * (self.tapEndwidth + config.dfPosOptCellOpening)

        rec0 = gdspy.Polygon([(xpos, ypos), (xup, yup), (xdown, ydown)])

        circle1 = gdspy.boolean(Poscircle, circle, "not", max_points=config.MAXPOINTS, layer=self.openinglayer)



        tapper0 = gdspy.boolean(circle1, rec0, "not", max_points=config.MAXPOINTS, layer=self.openinglayer)

        patterns.append(tapper0)

        # rtmp = self.tapRadius + posdist + 0.002
        # corc1x, corc1y = self._step(xpos, ypos, rtmp * np.cos( diffang ) )
        # xPosup, yPosup = corc1x + nx * (self.tapEndwidth + config.dfPosOptCellOpening), corc1y + ny * (self.tapEndwidth + config.dfPosOptCellOpening)
        # xPosdown, yPosdown = corc1x - nx * (self.tapEndwidth + config.dfPosOptCellOpening), corc1y - ny * (self.tapEndwidth + config.dfPosOptCellOpening)


        # grating lines
        thick = self.gDuty * self.gPeriod
        rcur -= thick / 2.

        for i in range(self.gN):

            diffang = np.arctan2(wcur / 2.0, rcur)
            gratcircle = gdspy.Round((x0, y0), rcur + thick, rcur ,
                                     initial_angle=dirRad - diffang, final_angle=dirRad + diffang,
                                     max_points=config.MAXPOINTS,
                                     layer=self.openinglayer
                                     )
            patterns.append(gratcircle)
            rcur += self.gPeriod

        self.add(patterns)

        pass

    def _step(self, x, y, step):
        x1 = x + step * self._dx
        y1 = y + step * self._dy
        return x1, y1

    # end of PosOptSimpleGratingCoupler





def _createEtchPath(path, etchlayer, straight=False):

    shapes = []
    connectFlag = True
    Lend = len(path)

    currentNodesPlus = []
    currentNodesMinus = []
    (xlast, ylast) = path[0]
    FlagFirstpoint = True
    pathtmp = np.concatenate((path[1:Lend],np.array([path[-1]])))  # ensure the last point is added.
    for (xcurrent, ycurrent) in pathtmp:    #added skip path to reduce resolution, --> fast and small file sizes
        dx = xcurrent - xlast
        dy = ycurrent - ylast
        dxn = -dy
        dyn = dx
        if float(dxn * dxn + dyn * dyn)< 1e-8:   # skip repeated points
            continue
        revl = 1.0 / sqrt(float(dxn * dxn + dyn * dyn))
        dxn *= revl
        dyn *= revl

        if FlagFirstpoint:
            nodePlus = (xlast + dxn * (config.dfoptwgwidth + config.dfPosOptCellOpening )*0.5,
                        ylast + dyn * (config.dfoptwgwidth + config.dfPosOptCellOpening )*0.5)
            nodeMinus = (xlast - dxn* (config.dfoptwgwidth + config.dfPosOptCellOpening )*0.5,
                         ylast - dyn * (config.dfoptwgwidth + config.dfPosOptCellOpening )*0.5)
            currentNodesPlus.append(nodePlus)
            currentNodesMinus.append(nodeMinus)
            FlagFirstpoint = False


        nodePlus = (xcurrent + dxn  * (config.dfoptwgwidth + config.dfPosOptCellOpening )*0.5,
                    ycurrent + dyn  * (config.dfoptwgwidth + config.dfPosOptCellOpening )*0.5)
        nodeMinus = (xcurrent - dxn  * (config.dfoptwgwidth + config.dfPosOptCellOpening )*0.5,
                     ycurrent - dyn  * (config.dfoptwgwidth + config.dfPosOptCellOpening )*0.5)
        currentNodesPlus.append(nodePlus)
        currentNodesMinus.append(nodeMinus)
        xlast = xcurrent
        ylast = ycurrent

    if straight:
        shapes.append(gdspy.FlexPath([currentNodesPlus[0],currentNodesPlus[-1]], config.dfPosOptCellOpening, layer=etchlayer))
        shapes.append(gdspy.FlexPath([currentNodesMinus[0],currentNodesMinus[-1]], config.dfPosOptCellOpening, layer=etchlayer))
    else:
        shapes.append(gdspy.FlexPath(currentNodesPlus, config.dfPosOptCellOpening, layer=etchlayer, max_points=config.MAXPOINTS))
        shapes.append(gdspy.FlexPath(currentNodesMinus, config.dfPosOptCellOpening, layer=etchlayer, max_points=config.MAXPOINTS))
        # print("[DEBUG]")
        # print("PlusNodes:")
        # print(currentNodesPlus)

    return shapes


def _pointDist(a, b):
    return sqrt(float(a[0] - b[0]) ** 2 + float(a[1] - b[1]) ** 2)

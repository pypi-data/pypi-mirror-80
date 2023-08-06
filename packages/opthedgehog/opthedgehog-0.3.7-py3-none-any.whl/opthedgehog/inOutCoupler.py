from math import sqrt
import numpy as np
import warnings



from .optCells import *
from .optCells import _normalizedxdy, _taperPath
from .suspendedOptCell import _createsuspath, _safepathnodes

from . import config


class OptSimpleGratingCoupler(OptCell):
    """
    Rectangular gating for in and out coupler.

    Args:
        name: str,
        inports: List[Tuple[float, float, float, float]]
        gratingN: int -- Number of the grating period.
        gratingPeroid: float -- Pitch of the grating.
        reverse: bool, default False  -- If *False*, the waveguide connects to the **outports**; if *True*, the waveguide connects to **inports**.
        taperLength: float, default *400.0*
        gratingApod: bool, default *False* -- If *True*, it creates apodized grating (varying in grating duty).
        gratingWidth: float, default *13.0*
        gratingExt: float, default *5.0*
        gratingDuty: float, default *0.5*
        layer: int, default *10*

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width

    Example:
        >>> gratingIN = opthedgehog.OptSimpleGratingCoupler("OptSimpleGratingCoupler", inports=[(100, 300, 9.0, 0.5)], gratingN=40, gratingPeroid=0.8, gratingApod=True, gratingWidth=20.0, gratingDuty=0.25)
        >>> gratingOUT = opthedgehog.OptSimpleGratingCoupler("OptSimpleGratingCoupler", inports=gratingIN.outports, gratingN=40, gratingPeroid=0.8, reverse=True)

    """

    #direction of the grating coupling
    reverse = False

    #grating parameters
    gN : int = 0
    gPeriod = 1.0
    gDuty = 1.0
    gApodized = False
    gWidth = 0.0
    gExt = 0.0

    #tapering
    tapLen = 0.0
    tapEndwidth = 0.0

    #internal cariables
    _dx = 0.0
    _dy = 0.0
    _nx = 0.0
    _ny = 0.0

    def __init__(self, name: str,
                 inports: List[Tuple[float, float, float, float]],
                 gratingN: int,
                 gratingPeroid: float,
                 reverse = False,
                 *,
                 taperLength = 400.0,  # the length of the taper
                 gratingApod: bool = False,
                 gratingWidth = 13.0,
                 gratingExt = 5.0,
                 gratingDuty:float = 0.5,
                 layer=10):
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
        self.gApodized = gratingApod
        self.gWidth = gratingWidth
        self.gExt = gratingExt

        self.tapLen = taperLength
        self.tapEndwidth = config.dfoptwgwidth

        #calculate outports
        xend, yend = self._step(x0, y0, self.gExt * 2.0 + self.gPeriod * self.gN + self.tapLen)
        self.outports = [(xend, yend, dx, dy)]

        #mask
        self.createMask()
        #outports not generated here.

    def createMask(self):
        if self.reverse:
            (x0, y0, dx, dy ) = self.outports[0]
            dx, dy = -dx, -dy
        else:
            (x0, y0, dx, dy ) = self.inports[0]

        dx, dy = _normalizedxdy(dx, dy)  # propogation direction
        nx, ny = dy, -dx  # normal vector
        self._dx = dx
        self._dy = dy
        self._nx = nx
        self._ny = ny

        #lower bound corrdinates
        xlow, ylow = x0 - nx * self.gWidth *0.5, y0 - ny * self.gWidth * 0.5

        #upp bound corrdinates
        xupp, yupp = x0 + nx * self.gWidth *0.5, y0 + ny * self.gWidth * 0.5

        patterns = []

        #first end extent zone
        xlow2, ylow2 = self._step(xlow, ylow, self.gExt)
        xupp2, yupp2 = self._step(xupp, yupp, self.gExt)

        ext1 = gdspy.Polygon([ (xlow, ylow), (xlow2, ylow2), (xupp2, yupp2), (xupp, yupp)], layer = self.layer)
        patterns.append(ext1)

        xlow, ylow = xlow2, ylow2
        xupp, yupp = xupp2, xupp2


        #grating
        for i in range(0, self.gN):
            #calculate the opening width
            if self.gApodized:
                alpha = float(i) / self.gN
                owidth = self.gPeriod * self.gDuty * (1.0 - alpha**2.73654873)   #just a random number
            else:
                owidth = self.gPeriod * self.gDuty

            xlow, ylow = self._step(xlow2, ylow2, owidth)
            xupp, yupp = self._step(xupp2, yupp2, owidth)
            xlow2, ylow2 = self._step(xlow2, ylow2, self.gPeriod)
            xupp2, yupp2 = self._step(xupp2, yupp2, self.gPeriod)

            gratingline = gdspy.Polygon([ (xlow, ylow), (xlow2, ylow2), (xupp2, yupp2), (xupp, yupp)], layer = self.layer)
            patterns.append(gratingline)

        #waveguide end ext
        xlow, ylow = xlow2, ylow2
        xupp, yupp = xupp2, yupp2
        xlow2, ylow2 = self._step(xlow2, ylow2, self.gExt)
        xupp2, yupp2 = self._step(xupp2, yupp2, self.gExt)

        ext2 = gdspy.Polygon([(xlow, ylow), (xlow2, ylow2), (xupp2, yupp2), (xupp, yupp)], layer=self.layer)
        patterns.append(ext2)

        #taper to end
        xc = (xlow2 + xupp2) / 2.0
        yc = (ylow2 + yupp2) / 2.0
        patterns.append(_taperPath( [(xc, yc), self._step(xc, yc, self.tapLen)], [self.gWidth, self.tapEndwidth], self.layer))

        self.add(patterns)

        pass

    def _step(self, x, y, step):
        x1 = x + step*self._dx
        y1 = y + step*self._dy
        return x1, y1

    #end of OptSimpleGratingCoupler


class OptCurvedGratingCoupler(OptCell):
    """
    Curved gating for in and out coupler. Better for shorter taper length

    Args:
        name: str,
        inports: List[Tuple[float, float, float, float]]
        gratingN: int -- Number of the grating period.
        gratingPeroid: float -- Pitch of the grating.
        reverse: bool, default False  -- If *False*, the waveguide connects to the **outports**; if *True*, the waveguide connects to **inports**.
        focusRadius: float, default *400.0* -- The radius of the first grating line to the waveguide.
        gratingWidth: float, default *13.0*
        gratingDuty: float, default *0.5*
        layer: int, default *10*

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width

    Example:
        >>> Curvedgrt1 = opthedgehog.OptCurvedGratingCoupler("OptCurvedGratingCoupler", inports=[(-1000, 700, 1.0, -0.3)], gratingN= 20, gratingPeroid=1. , focusRadius=50., layer = 1)
        >>> Curvedgrt2 = opthedgehog.OptCurvedGratingCoupler("OptCurvedGratingCoupler", inports=wgH1.outports, gratingN=20, gratingPeroid=1., reverse=True, layer = 1)

    """

    #direction of the grating coupling
    reverse = False

    #grating parameters
    gN : int = 0
    gPeriod = 1.0
    gDuty = 1.0
    gWidth = 0.0

    #tapering
    rext = 0.0
    tapRadius = 0.0
    tapLen = 0.0
    tapEndwidth = 0.0

    #internal cariables
    _dx = 0.0
    _dy = 0.0
    _nx = 0.0
    _ny = 0.0

    def __init__(self, name: str,
                 inports: List[Tuple[float, float, float, float]],
                 gratingN: int,
                 gratingPeroid: float,
                 reverse = False,
                 *,
                 focusRadius = 20.0,  # the Radius of focusing waveguide
                 gratingWidth = 13.0,
                 gratingDuty:float = 0.5,
                 layer=10):
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

        #calculate tap lens
        w1 = gratingWidth
        r1 = focusRadius
        w0 = self.tapEndwidth
        r0 = w0 * r1 / w1
        #   w1        w0
        #  ----- == ------
        #   r1        r0
        self.rext = r0
        self.tapLen = focusRadius - r0

        #calculate outports
        xend, yend = self._step(x0, y0, self.gPeriod * self.gN + self.tapLen)
        self.outports = [(xend, yend, dx, dy)]

        #mask
        self.createMask()
        #outports not generated here.

    def createMask(self):
        if self.reverse:
            (x0, y0, dx, dy ) = self.inports[0]
            x0, y0 = self._step(x0, y0, -self.rext)

        else:
            (x0, y0, dx, dy ) = self.outports[0]
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

        #taper waveguide
        wcur = self.gWidth
        rcur = self.tapRadius

        diffang = np.arctan2( wcur/2.0, rcur)

        circle = gdspy.Round( (x0, y0), self.tapRadius,
                              initial_angle= dirRad-diffang, final_angle = dirRad+diffang,
                              max_points = config.MAXPOINTS,

                              )
        xc1,yc1 = self._step(x0, y0, self.rext-0.001)
        xup, yup = xc1 + nx * self.tapEndwidth,  yc1 + ny * self.tapEndwidth
        xdown, ydown = xc1 - nx * self.tapEndwidth, yc1 - ny * self.tapEndwidth

        rec0 = gdspy.Polygon( [(x0,y0), (xup, yup), (xdown, ydown)])
        tapper0 = gdspy.boolean(circle, rec0, "not",  max_points=config.MAXPOINTS, layer = self.layer)

        patterns.append(tapper0)

        #grating lines
        thick = self.gDuty * self.gPeriod
        rcur -= thick / 2.

        for i in range(self.gN):
            rcur += self.gPeriod
            diffang = np.arctan2(wcur / 2.0, rcur)
            gratcircle = gdspy.Round( (x0, y0), rcur + thick/2., rcur - thick/2.,
                                        initial_angle= dirRad-diffang, final_angle = dirRad+diffang,
                                        max_points = config.MAXPOINTS,
                                        layer = self.layer
                                    )
            patterns.append(gratcircle)

        self.add(patterns)

        pass

    def _step(self, x, y, step):
        x1 = x + step*self._dx
        y1 = y + step*self._dy
        return x1, y1

    #end of OptCurvedGratingCoupler



class OptSuspnededFiberTipCoupler(OptCell):
    """
    Suspended tapered waveguide for coupling method using fiber tip touching

    Args:
        name: str,
        inports: List[Tuple[float, float, float, float]],
        L1: float,  design parameter see images below
        W1: float,  design parameter see images below
        L2: float,  design parameter see images below
        S2: float,  design parameter see images below
        Ext: float,  design parameter see images below
        tipTopWidth: float = 0.05,
        tipSlabWidth: float = 0.35,
        reverse: bool = False,    *False* for the *outports* connects to the waveguide; *True* for *inports* connects to the waveguide.
        layer:int = 10,  top optical waveguide layer
        suslayer: int = 20,    slab etching layer

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width

     Example:
         >>> fibertaper1 = opthedgehog.OptSuspnededFiberTipCoupler("OptSuspnededFiberTipCoupler", inports=[(0., 0., 1., 0.)], L1 = 40, W1=1.5, L2 = 25, S2 = 8, Ext=150.)

    """

    L1 = 0.0
    W1 = 0.0
    L2 = 0.0
    W2 = 0.0
    S2 = 0.0
    Ext = 0.0
    tipTopWidth = 0.0
    tipSlabWidth = 0.0
    suspendedTop = False

    reverse = False
    suslayer = 0

    def __init__(self, name: str,
                 inports: List[Tuple[float, float, float, float]],
                 L1: float,
                 W1: float,
                 L2: float,
                 S2: float,
                 Ext: float,
                 *,
                 tipTopWidth: float = 0.05,
                 tipSlabWidth: float = 0.28,
                 reverse: bool = False,
                 suspendedTop: bool = False,
                 layer:int = 10,
                 suslayer: int = 20,
                 ):
        OptCell.__init__(self, name, layer)
        self.L1 = L1
        self.W1 = W1
        self.L2 = L2
        self.W2 = config.dfoptwgwidth
        self.S2 = S2
        self.Ext = Ext
        self.tipTopWidth = tipTopWidth
        self.tipSlabWidth = tipSlabWidth
        self.suspendedTop = suspendedTop

        self.reverse = reverse
        self.suslayer = suslayer

        self.inports = inports

        self.createMask()

        pass

    def createMask(self):
        Ltot = self.L2 + self.L1 - self.S2 + self.Ext

        if self.reverse:
            x0, y0, dx0, dy0 = self.inports[0]
            dx0, dy0 = _normalizedxdy(dx0, dy0)
            nx0, ny0 = -dy0, dx0

            xend = x0 + dx0 * Ltot
            yend = y0 + dy0 * Ltot
            self.outports = [(xend, yend, dx0, dy0)]
        else:
            xend, yend, dx0, dy0 = self.inports[0]

            x0 = xend + dx0 * Ltot
            y0 = yend + dy0 * Ltot
            self.outports = [(x0, y0, dx0, dy0)]
            dx0 = -dx0
            dy0 = -dy0
            nx0, ny0 = -dy0, dx0

        #toplayer Taper
        xtop = x0 + nx0 * self.W2 / 2.
        ytop = y0 + ny0 * self.W2 / 2.
        xbtm = x0 - nx0 * self.W2 / 2.
        ybtm = y0 - ny0 * self.W2 / 2.
        xtip = x0 + dx0 * self.L2
        ytip = y0 + dy0 * self.L2

        if self.tipTopWidth > 1E-6:
            xtipup = x0 + dx0 * self.L2 + nx0 * self.tipTopWidth / 2.
            ytipup = y0 + dy0 * self.L2 + ny0 * self.tipTopWidth / 2.
            xtipbt = x0 + dx0 * self.L2 - nx0 * self.tipTopWidth / 2.
            ytipbt = y0 + dy0 * self.L2 - ny0 * self.tipTopWidth / 2.
            topwg = gdspy.Polygon([(xtop, ytop), (xbtm, ybtm), (xtipbt, ytipbt), (xtipup, ytipup)], layer=self.layer)
            self.add(topwg)

        else:
            topwg = gdspy.Polygon( [(xtop, ytop), (xbtm, ybtm), (xtip, ytip)], layer=self.layer )
            self.add(topwg)

        if self.suspendedTop:
            #print(f"debug {[(x0, y0), (xtip, ytip)]=}")
            o1 = _createsuspath(_safepathnodes([(x0, y0), (xtip, ytip)]), suslayer=self.suslayer)
            self.add(o1)


        #bottom opening
        D2 = self.L2 - self.S2
        wext = max(5.*self.W1, 10.)

        points = []
        xoutP = x0 + dx0 * D2 + nx0 * (self.W2 / 2. + wext)
        youtP = y0 + dy0 * D2 + ny0 * (self.W2 / 2. + wext)
        points.append((xoutP, youtP))

        xbaseP = x0 + dx0 * D2 + nx0 * self.W1 / 2.
        ybaseP = y0 + dy0 * D2 + ny0 * self.W1 / 2.
        points.append((xbaseP, ybaseP))

        Dtip = self.L2 + self.L1 - self.S2
        xtipP = x0 + dx0 * Dtip + nx0 * self.tipSlabWidth / 2.
        ytipP = y0 + dy0 * Dtip + ny0 * self.tipSlabWidth / 2.
        xtipN = x0 + dx0 * Dtip - nx0 * self.tipSlabWidth / 2.
        ytipN = y0 + dy0 * Dtip - ny0 * self.tipSlabWidth / 2.
        points.append((xtipP, ytipP))
        if self.tipSlabWidth > 1E-6:
            points.append((xtipN, ytipN))

        xbaseN = x0 + dx0 * D2 - nx0 * self.W1 / 2.
        ybaseN = y0 + dy0 * D2 - ny0 * self.W1 / 2.
        points.append((xbaseN, ybaseN))

        xoutN = x0 + dx0 * D2 - nx0 * (self.W2 / 2. + wext)
        youtN = y0 + dy0 * D2 - ny0 * (self.W2 / 2. + wext)
        points.append((xoutN, youtN))

        xoutN2 = x0 + dx0 * (Dtip+self.Ext) - nx0 * (self.W2 / 2. + wext)
        youtN2 = y0 + dy0 * (Dtip+self.Ext) - ny0 * (self.W2 / 2. + wext)
        points.append((xoutN2, youtN2))

        xoutP2 = x0 + dx0 * (Dtip + self.Ext) + nx0 * (self.W2 / 2. + wext)
        youtP2 = y0 + dy0 * (Dtip + self.Ext) + ny0 * (self.W2 / 2. + wext)
        points.append((xoutP2, youtP2))

        openEtch = gdspy.Polygon( points, layer=self.suslayer )
        self.add(openEtch)

        pass



class OptSuspnededFiberTipCouplerConnected(OptCell):
    """
    Suspended tapered waveguide for coupling method using fiber tip touching
    Connection at taperend.

    Args:
        name: str,
        inports: List[Tuple[float, float, float, float]],
        L1: float,  design parameter see images below
        W1: float,  design parameter see images below
        L2: float,  design parameter see images below
        S2: float,  design parameter see images below
        Ext: float,  design parameter see images below
        tipTopWidth: float = 0.05,
        tipSlabWidth: float = 0.35,
        reverse: bool = False,    *False* for the *outports* connects to the waveguide; *True* for *inports* connects to the waveguide.
        layer:int = 10,  top optical waveguide layer
        suslayer: int = 20,    slab etching layer

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width

     Example:
         >>> fibertaper1 = opthedgehog.OptSuspnededFiberTipCoupler("OptSuspnededFiberTipCoupler", inports=[(0., 0., 1., 0.)], L1 = 40, W1=1.5, L2 = 25, S2 = 8, Ext=150.)

    """

    L1 = 0.0
    W1 = 0.0
    L2 = 0.0
    W2 = 0.0
    S2 = 0.0
    Ext = 0.0
    tipTopWidth = 0.0
    tipSlabWidth = 0.0
    suspendedTop = False

    reverse = False
    suslayer = 0

    def __init__(self, name: str,
                 inports: List[Tuple[float, float, float, float]],
                 L1: float,
                 W1: float,
                 L2: float,
                 S2: float,
                 Ext: float,
                 *,
                 tipTopWidth: float = 0.05,
                 tipSlabWidth: float = 0.28,
                 reverse: bool = False,
                 suspendedTop: bool = False,
                 layer:int = 10,
                 suslayer: int = 20,
                 ):
        OptCell.__init__(self, name, layer)
        self.L1 = L1
        self.W1 = W1
        self.L2 = L2
        self.W2 = config.dfoptwgwidth
        self.S2 = S2
        self.Ext = Ext
        self.tipTopWidth = tipTopWidth
        self.tipSlabWidth = tipSlabWidth
        self.suspendedTop = suspendedTop

        self.reverse = reverse
        self.suslayer = suslayer

        self.inports = inports

        self.createMask()

        pass

    def createMask(self):
        Ltot = self.L2 + self.L1 - self.S2 + self.Ext

        if self.reverse:
            x0, y0, dx0, dy0 = self.inports[0]
            dx0, dy0 = _normalizedxdy(dx0, dy0)
            nx0, ny0 = -dy0, dx0

            xend = x0 + dx0 * Ltot
            yend = y0 + dy0 * Ltot
            self.outports = [(xend, yend, dx0, dy0)]
        else:
            xend, yend, dx0, dy0 = self.inports[0]

            x0 = xend + dx0 * Ltot
            y0 = yend + dy0 * Ltot
            self.outports = [(x0, y0, dx0, dy0)]
            dx0 = -dx0
            dy0 = -dy0
            nx0, ny0 = -dy0, dx0

        #toplayer Taper
        xtop = x0 + nx0 * self.W2 / 2.
        ytop = y0 + ny0 * self.W2 / 2.
        xbtm = x0 - nx0 * self.W2 / 2.
        ybtm = y0 - ny0 * self.W2 / 2.
        xtip = x0 + dx0 * self.L2
        ytip = y0 + dy0 * self.L2

        if self.tipTopWidth > 1E-6:
            xtipup = x0 + dx0 * self.L2 + nx0 * self.tipTopWidth / 2.
            ytipup = y0 + dy0 * self.L2 + ny0 * self.tipTopWidth / 2.
            xtipbt = x0 + dx0 * self.L2 - nx0 * self.tipTopWidth / 2.
            ytipbt = y0 + dy0 * self.L2 - ny0 * self.tipTopWidth / 2.
            topwg = gdspy.Polygon([(xtop, ytop), (xbtm, ybtm), (xtipbt, ytipbt), (xtipup, ytipup)], layer=self.layer)
            self.add(topwg)

        else:
            topwg = gdspy.Polygon( [(xtop, ytop), (xbtm, ybtm), (xtip, ytip)], layer=self.layer )
            self.add(topwg)

        if self.suspendedTop:
            #print(f"debug {[(x0, y0), (xtip, ytip)]=}")
            o1 = _createsuspath(_safepathnodes([(x0, y0), (xtip, ytip)]), suslayer=self.suslayer)
            self.add(o1)


        #bottom opening
        D2 = self.L2 - self.S2
        wext = max(5.*self.W1, 10.)

        points = []
        xoutP = x0 + dx0 * D2 + nx0 * (self.W2 / 2. + wext)
        youtP = y0 + dy0 * D2 + ny0 * (self.W2 / 2. + wext)
        points.append((xoutP, youtP))

        xbaseP = x0 + dx0 * D2 + nx0 * self.W1 / 2.
        ybaseP = y0 + dy0 * D2 + ny0 * self.W1 / 2.
        points.append((xbaseP, ybaseP))

        Dtip = self.L2 + self.L1 - self.S2
        xtipP = x0 + dx0 * Dtip + nx0 * self.tipSlabWidth / 2.
        ytipP = y0 + dy0 * Dtip + ny0 * self.tipSlabWidth / 2.
        xtipN = x0 + dx0 * Dtip - nx0 * self.tipSlabWidth / 2.
        ytipN = y0 + dy0 * Dtip - ny0 * self.tipSlabWidth / 2.
        points.append((xtipP, ytipP))
        if self.tipSlabWidth > 1E-6:
            points.append((xtipN, ytipN))

        xbaseN = x0 + dx0 * D2 - nx0 * self.W1 / 2.
        ybaseN = y0 + dy0 * D2 - ny0 * self.W1 / 2.
        points.append((xbaseN, ybaseN))

        xoutN = x0 + dx0 * D2 - nx0 * (self.W2 / 2. + wext)
        youtN = y0 + dy0 * D2 - ny0 * (self.W2 / 2. + wext)
        points.append((xoutN, youtN))

        xoutN2 = x0 + dx0 * (Dtip+self.Ext) - nx0 * (self.W2 / 2. + wext)
        youtN2 = y0 + dy0 * (Dtip+self.Ext) - ny0 * (self.W2 / 2. + wext)
        points.append((xoutN2, youtN2))

        xoutP2 = x0 + dx0 * (Dtip + self.Ext) + nx0 * (self.W2 / 2. + wext)
        youtP2 = y0 + dy0 * (Dtip + self.Ext) + ny0 * (self.W2 / 2. + wext)
        points.append((xoutP2, youtP2))

        #addtopconnection
        xtipe = x0 + dx0 * (Dtip + 1.5)
        ytipe = y0 + dy0 * (Dtip + 1.5)
        xtip = x0 + dx0 * (Dtip)
        ytip = y0 + dy0 * (Dtip)
        xcontop1 = xoutP + dx0 * (Dtip - D2 + 5.)
        ycontop1 = youtP + dy0 * (Dtip - D2 + 5.)
        topcon1 = gdspy.Polygon( [(xtipe, ytipe), (xtip, ytip), (xtipP, ytipP), (xcontop1, ycontop1), (xoutP2, youtP2)], layer=self.suslayer )

        xtipe = x0 + dx0 * (Dtip + 1.5)
        ytipe = y0 + dy0 * (Dtip + 1.5)
        xtip = x0 + dx0 * (Dtip)
        ytip = y0 + dy0 * (Dtip)
        xcontop1 = xoutN + dx0 * (Dtip - D2 + 5.)
        ycontop1 = youtN + dy0 * (Dtip - D2 + 5.)
        topcon2 = gdspy.Polygon([(xtipe, ytipe), (xtip, ytip), (xtipN, ytipN), (xcontop1, ycontop1), (xoutN2, youtN2)], layer=self.suslayer)


        openEtch = gdspy.Polygon( points, layer=self.suslayer )

        merge = gdspy.boolean(openEtch, topcon1, "not", layer=self.suslayer)
        merge = gdspy.boolean(merge, topcon2, "not", layer=self.suslayer)
        self.add(merge)

        pass






class SuspendedTaperCoupler(OptCell):
    """

    """
    suslayer = 20
    wgtaper = 0.0
    wgtaperend = 0.0
    slabtaper = 0.0
    slabend = 0.0
    direction = -1
    taperp = 1.0
    totiplength = -1.0
    def __init__(self, name, port, wgtaper, wgtaperend, slabtaper, slabend, direction, optlayer = 10, suslayer = 20, taperp = 1.0, totiplength = -1.0):
        """
        :param name:
        :param port:
        :param wgtaper:
        :param wgtaperend:
        :param slabtaper:
        :param slabend:
        :param direction:
        :param optlayer:
        :param suslayer:
        :param tapermtd:
        """
        OptCell.__init__(self, name, optlayer)

        self.suslayer = suslayer
        if isinstance(port, list):
            self.inports = port
            if len(port) > 1:
                warnings.warn("[OptHedgehog WARNING] SuspendedTaperCoupler found more that one inports, first port of "+str(port)+" is used.")
        else:
            self.inports.append(port)

        self.outports = self.inports
        self.wgtaper = wgtaper
        self.wgtaperend = wgtaperend
        self.slabtaper = slabtaper
        self.slabend = slabend
        self.direction = direction
        self.taperp = taperp
        self.totiplength = totiplength

        self.createMask()
        pass

    def createMask(self):
        (x0, y0, tmp, tmp) = self.inports[0]


        #align the tapertip for different size of tapers
        if self.totiplength <= 0.0:
            x1 = x0 + config.dfOpeningConnection*self.direction
            y1 = y0
        elif self.totiplength - self.slabtaper < 0.0:
            warnings.warn("[OptHedgehog WARNING] SuspendedTaperCoupler ToTipLength "+str(self.totiplength)+" shorter than slab taper length "+str(self.slabtaper))
            return -1
        elif self.totiplength - self.slabtaper < 3.0:
            dist = self.totiplength - self.slabtaper
            x1 = x0 + dist*self.direction
            y1 = y0
        else:
            dist = self.totiplength - self.slabtaper - 3.0
            x1 = x0 + (self.totiplength - self.slabtaper)*self.direction
            y1 = y0
            N = dist / 0.1 + 3
            nodes = [(x0 + i * dist * self.direction , y0) for i in np.arange(0.0, 1.0, 1.0 / N)]
            addopencell = _createsuspath(nodes, suslayer=self.suslayer)
            self.add(addopencell)
            ######################## stop here #####################




        #support connection
        wg1 = gdspy.PolyPath([(x0, y0), (x1, y0)], width = config.dfoptwgwidth, layer = self.layer)
        self.add(wg1)

        #taper waveguide, linear
        x2 = x1 + self.wgtaper * self.direction
        y2 = y1
        dyend = self.wgtaperend / 2.0
        dy = config.dfoptwgwidth / 2.0
        taper2 = gdspy.Polygon([ (x1, y1 + dy), (x2, y2 + dyend), (x2, y2 - dyend), (x1, y1 - dy) ], layer = self.layer)
        self.add(taper2)

        # slab taper
        x3 = x1 + self.slabtaper * self.direction
        y3 = y1
        dy = config.dfoptwgwidth*2.0
        dyend = self.slabend / 2.0
        Dy = dy - dyend
        N = int(abs(x3-x1) / 0.05 + 2)
        lx = np.linspace(x3, x1, N)
        p = self.taperp
        ly = y3 + (np.fabs(lx-x3)**p)/(np.fabs(x1-x3)**p) * Dy + dyend
        points = np.transpose([lx, ly])

        lx2 = np.linspace(x1, x3, N)
        ly2 = y3 - (np.fabs(lx2 - x3) ** p) / (np.fabs(x1 - x3) ** p) * Dy - dyend
        points2 = np.transpose([lx2, ly2])
        listpoints = np.concatenate((points, points2), axis = 0)
        slabShape = gdspy.Polygon(listpoints)
        # slabShape.fracture(max_points=199)

        ydown = y3 - config.dfOpeningOffset*2 - config.dfOpeningWidth
        yup = y3 + config.dfOpeningOffset*2 + config.dfOpeningWidth
        rect = gdspy.Rectangle( (x3 + 100.0*self.direction, ydown), (x1 + 7.0*self.direction, yup))

        opening = gdspy.fast_boolean(rect, slabShape, "not", layer = self.suslayer, max_points=199)
        self.add(opening)

        #dicing guideline
        guideline = gdspy.PolyPath([(x3 + 100.0*self.direction, y3 + 15.0), (x3+ 100.0*self.direction , y3 - 15.0)], width = 1.0, layer = self.suslayer)
        self.add(guideline)

        pass


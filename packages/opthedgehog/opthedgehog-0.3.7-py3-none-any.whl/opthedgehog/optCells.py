#########################################################
##  Hedgehog ---                                      ###
##   A Python package for integreated optices.        ###
##  Description:
##     This files contains functions to generate basic optical elements ###
#########################################################

from gdspy import Cell
import gdspy
import numpy as np
import bezier
import warnings
from typing import Tuple, List, Union
from termcolor import colored

#from config import dfoptwgwidth, _index
# The above import won't be sync'ed globally, and only take the value initionalized and not follew the change.

from . import config


class OptCell(Cell):
    """
    Base class of all optial component cells

    Args:
        name (str):
            Name of the cell
        layer (int):
            The gds layer number of the main optical components, e.g. waveguides.
    """

    layer = 10  #. gds layer
    currentconfig = None
    rawname = ""

    inports:List[Tuple[float, float, float, float]] = []
    """ List of input optical ports
    
        Each port is defined by a tuple (*x*, *y*, *dx*, *dy*). *x, y* define the position, and *dx, dy* define the direction. 
        
        For example:  *(10., 20., 1., 0.)* defines the port at *(10., 20.)* pointing to the *x+* axis.  
    """

    outports:List[Tuple[float, float, float, float]]
    """
    List of output optical ports
        
    Note
    ----
    The **outports** are automatically calculated in the code. **DO NOT CHANGE.** 
    """

    def __init__(self, name: str, layer:int=10):
        name0 = name + "_%d" % (config._index())
        gdspy.Cell.__init__(self, name0)
        self.layer = layer
        self.inports = []
        self.outports = []
        self.rawname = name

        self.copylocalconfig()
        #added 3/18/2020

    def copylocalconfig(self):
        self.currentconfig = {}
        for var in dir(config):
            if var[:2] == "df":
                self.currentconfig[var] = getattr(config, var)

    def addLabel(self):
        posx, posy, tmp, tmp = self.inports[0]
        label1 = gdspy.Label(self.rawname, (posx, posy), 'sw', layer=self.layer)
        self.add(label1)


class OptStraightWaveguide(OptCell):
    """
    Straight waveguide

    Args:
        name: str
        inports: List[Tuple[float, float, float, float]]
        length: float
        layer: int
        endwidth: float

          *default* or *endwidth < 0 *, the waveguide width will keep unchanged.
          *endwidth >= 0.*, the waveguide width will be linearly tapered to *endwidth*

          **Note:** the global setting config.dfoptwgwidth will be automatically changed to the endwidth, if setted.

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width

    Example
    -------
        >>>  wg1 = opthedgehog.OptStraightWaveguide("OptStraightWaveguide", inports=[(0, 600, 1.0, 0.)], length=400)
    """

    # on date July 29, 2019 -- revise to straight waveguide in any direction, defined bu the input port
    length = 0.0
    endwidth = 0.0
    arc = 0.0

    def __init__(self, name, inports: List[Tuple[float, float, float, float]], length:float, layer:int=10, *, endwidth = -1.0):
        """
        """

        # update  Dec 11, 2019, add endwith to allow linear tapering of the waveguide.
        OptCell.__init__(self, name, layer)
        if isinstance(inports, list):
            self.inports = inports
        else:
            self.inports.append(inports)

        if endwidth < -0.1:
            self.endwidth = config.dfoptwgwidth
        else:
            self.endwidth = endwidth
            print( colored(f"[optohedgehog WARNING] tapering optical waveguide, the global setting *config.dfoptwgwidth* changed to {endwidth}.", "blue"))

        self.length = length
        self.pathnodes = []
        (x, y, dx, dy) = self.inports[0]

        if dx*dx+dy*dy < 0.01:
            raise Exception("[opthedgehog] Value error","undefined waveguide direction at (%f,%f, %f,%f)"%(x,y,dx,dy))

        norm = np.sqrt(dx*dx+dy*dy)
        dx = dx / norm
        dy = dy / norm
        self.inports = [(x, y, dx, dy)]   # normailized the input direction

        self.arc = np.arctan2(dy, dx)

        xend = x + dx*length
        yend = y + dy*length

        self.outports = [(xend, yend, dx, dy)]

        self.createmask()

        # Create pathnodes for openings
        N = int(self.length / config.dfOptRes) + 5
        xlist = [x + dx * length * float(i) / float(N) for i in range(N)]
        xlist.append(xend)
        ylist = [y + dy * length * float(i) / float(N) for i in range(N)]
        ylist.append(yend)
        self.pathnodes = np.transpose([xlist,ylist])


    def createmask(self):
        """
        create mask for a waveguide
        :return: None
        """
        if len(self.inports) != 1 or len(self.outports) != 1:
            print("[OptHedgehog ERROR] straight waveguide only support one input and output, first port will be used. #in: %d, #out: %d"
                  % (len(self.inports), len(self.outports)))

        pos1 = (self.inports[0][0], self.inports[0][1])
        pos2 = (self.outports[0][0], self.outports[0][1])


        #Mar 14, 2020,   change PolyPath (Deprecated) to Path.
        wg1 = gdspy.Path(config.dfoptwgwidth, pos1,)
        wg1.segment(self.length, self.arc, final_width=self.endwidth, layer=self.layer)

        # wg1 = gdspy.PolyPath(points=[pos1, pos2], width=[config.dfoptwgwidth, self.endwidth], layer=self.layer)

        config.dfoptwgwidth = self.endwidth
        #updated Dec 11, 2019, automatically update the global parameter.
        self.add(wg1)


class OptBezierConnect(OptCell):
    """
    Bending waveguide using Bezier curve, defined by the shift from *inport* to *outport*, and the direction of the *outport*.

    **Note** If detailed control of the Bezier control points are required, use class *OptBezierWaveguide* instead.

    Args:
        name: str
        inports:  List[Tuple[float, float, float, float]]
        shift: Tuple[float, float]
        outputdirection: Tuple[float, float]
        layer: int

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width
        * config.dfTurningRadius: A reference parameter to generate the Bezier curve.

    Example
    -------
    >>> wg2 = opthedgehog.OptBezierConnect("OptBezierConnect", inports=wg1.outports, shift=(300,-50), outputdirection=(2.0, -0.5))
    """

    pathnodes = []  #. storage the nodes of the Bezier curve

    def __init__(self, name, inports, shift, outputdirection, layer=10):
        OptCell.__init__(self, name=name, layer=layer)
        if isinstance(inports, list):
            self.inports = inports
        else:
            self.inports = [inports]

        (x, y, dx, dy) = self.inports[0]


        self.outports = [(x + shift[0], y + shift[1], outputdirection[0], outputdirection[1])]
        self.pathnodes = []
        self.createmask()

    def createmask(self):
        (x0, y0, dx0, dy0) = self.inports[0]
        (xend, yend, dxend, dyend) = self.outports[0]

        norm0 = np.sqrt(dx0 * dx0 + dy0 * dy0)
        norm1 = np.sqrt(dxend * dxend + dyend * dyend)
        if norm0 < 0.1 or norm1 < 0.1:
            raise Exception("[optHedgehog] Value error","direction undefine, dx dy < 0.1")

        x1 = x0 + dx0 * config.dfTurningRadius / norm0
        y1 = y0 + dy0 * config.dfTurningRadius / norm0

        x2 = xend - dxend * config.dfTurningRadius / norm1
        y2 = yend - dyend * config.dfTurningRadius / norm1

        nodes = np.asfortranarray([
            [x0, x1, x2, xend],
            [y0, y1, y2, yend],
        ])
        curve = bezier.curve.Curve.from_nodes(nodes)

        dist = np.sqrt((yend - y0)*(yend - y0)+(xend - x0)*(xend - x0))
        segN = int(float(dist) / config.dfOptRes * 1.3 + 5)
        segs = np.linspace(0.0, 1.0, segN)
        nodes = curve.evaluate_multi(segs)

        nodes = np.transpose(nodes)
        self.pathnodes = nodes
        wg = gdspy.FlexPath(nodes, width=config.dfoptwgwidth, max_points=config.MAXPOINTS, layer=self.layer)
        self.add(wg)
        return None


    def calPathLength(self):
        d = 0.0
        x0, y0 = self.pathnodes[0]
        for x1, y1 in self.pathnodes[1:]:
            d += np.sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0))
            x0, y0 = x1, y1
        return d
    #end of OptBezierConnect


class OptBezierWaveguide(OptCell):
    """
    Bending waveguide using Bezier curve, defined by the **controlpoints** given by the user.

    The **controlpoints** is given in relative corrdinate to the **inport**. The curve will end at the last control point, the direction at the
    **outport** is defined by the last two control points.

    Args:
        name: str
        inports:  List[Tuple[float, float, float, float]]
        controlpoints: List[Tuple[float, float]]
        layer: int

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width

    Example
    -------
    >>> wg3 = opthedgehog.OptBezierWaveguide("OptBezierWaveguide", wg2.outports, [(100, 0), (200, 0), (250, 50)])

    """

    pathnodes = []  # store the nodes of the Bezier curve
    controlpoints = []  # store control poinst for Bezier .. this will not initialize at every __init__ cal!!!
    refLength :float = 0.0
    realLength :float = 0.0

    def __init__(self, name: str,
                 inports: List[Tuple[float,float,float,float]],
                 controlpoints: List[Tuple[float, float]],  # relative control points for Bezier curve, the inport is added automatically
                 *,
                 layer=10):
        OptCell.__init__(self, name=name, layer=layer)
        if isinstance(inports, list):
            self.inports = inports
        else:
            self.inports = [inports]

        # generate real control points list
        (x, y, dx, dy) = self.inports[0]
        self.refLength = 0.0
        self.controlpoints = [] # has to initial the list, other wise it contains from last class
        self.controlpoints.append( (x, y))
        lastx = lasty = 0.0
        for shiftx, shifty in controlpoints:
            self.controlpoints.append((x+shiftx, y+shifty))
            self.refLength += np.sqrt((shiftx-lastx)*(shiftx-lastx) + (shifty-lasty)*(shifty-lasty))
            lastx = shiftx
            lasty = shifty

        #calculate outports
        shiftx1, shifty1 = self.controlpoints[-1]
        shiftx2, shifty2 = self.controlpoints[-2]
        tmpdx = shiftx1 - shiftx2
        tmpdy = shifty1 - shifty2
        tmpl = 1.0 / np.sqrt(tmpdx*tmpdx + tmpdy*tmpdy)
        tmpdx *= tmpl
        tmpdy *= tmpl

        self.outports=[ (shiftx1, shifty1, tmpdx, tmpdy) ]


        self.createmask()

    def createmask(self):
        nodes = np.asfortranarray(np.transpose(self.controlpoints))
        curve = bezier.curve.Curve.from_nodes(nodes, )

        segN = int(float(self.refLength) / config.dfOptRes + 5)
        segs = np.linspace(0.0, 1.0, segN)
        nodes = curve.evaluate_multi(segs)

        nodes = np.transpose(nodes)
        self.pathnodes = nodes
        wg = gdspy.FlexPath(nodes, width=config.dfoptwgwidth, layer=self.layer, max_points=config.MAXPOINTS)
        self.add(wg)
        return None

    def calPathLength(self):
        d = 0.0
        x0, y0 = self.pathnodes[0]
        for x1, y1 in self.pathnodes[1:]:
            d += np.sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0))
            x0, y0 = x1, y1
        return d
    #end of class OptBezierWaveguide
    #end of OptBezierWaveguide


class OptCircularBend(OptCell):
    """
    Circular bending waveguide.

    Args:
        name: str
        inports: List[Tuple[float,float,float,float]]
        radius: float
        bendangle: float, bending angle in degrees, >0 for right hand bending.
        layer: int, default 10

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width

    Example
    -------
    >>> wg4 = opthedgehog.OptCircularBend("OptCircularBend", inports=wg3.outports, radius = 100.0, bendangle=90.0 )

    """
    r0 = 0.0
    a0 = 0.0
    p0 = 1.0

    def __init__(self, name: str,
                 inports: List[Tuple[float,float,float,float]],
                 radius: float,
                 bendangle: float, # bending angle in degrees, right hand position.
                 *,
                 layer=10):
        OptCell.__init__(self, name=name, layer=layer)
        self.inports = inports

        self.r0 = radius
        self.a0 = np.fabs(bendangle)/180.0*np.pi
        self.p0 = np.sign(bendangle)

        #outports calculated in the createmask function
        self.createmask()

    def createmask(self):

        (x0, y0, dx, dy) = self.inports[0]
        dx, dy = _normalizedxdy(dx, dy)


        nx = -dy*self.p0
        ny = dx*self.p0

        #center of radius
        cx = x0 + nx * self.r0
        cy = y0 + ny * self.r0
        start0 = np.arctan2(-ny, -nx)
        end0 = start0 + self.a0 * self.p0

        w0 = config.dfoptwgwidth

        curve = gdspy.Round(center = (cx, cy),
                            radius = self.r0 + w0/2.0,
                            inner_radius = self.r0 - w0/2.0,
                            initial_angle = start0,
                            final_angle= end0,
                            layer = self.layer,
                            max_points= config.MAXPOINTS)
        self.add(curve)

        # calculate outports
        xend = cx + self.r0 * np.cos(end0)
        yend = cy + self.r0 * np.sin(end0)
        ax = -np.sin(end0)*self.p0
        ay = np.cos(end0)*self.p0
        self.outports = [(xend, yend, ax, ay)]



class OptYsplitter(OptCell):
    """
    Y split waveguide.

    **splitshift** ( as a Tuple *(L, W)* ) defines the size of the Y splitter, length *L* in the direction of **inports[0]**,
    and *W* is the distance between two out ports.

    This class takes one in port and generates two out ports (as **outports[0]** and **outports[1]**).
    The direction of the **outports** will be same as the **inports**.

    Args:
        name: str
        inports: List[Tuple[float,float,float,float]]
        splitshift: Tuple[float, float]
        layer : int, *default: 10*

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width

    Example
    -------
    >>> wg5 = opthedgehog.OptYsplitter("OptYsplitter", inports=wg4.outports, splitshift=(200.0, 40.0))

    """
    # split one optical wave guide into two by 50/50 Y shape
    # Jan 2, 2020, update to any angle

    pathnodes1 = []
    pathnodes2 = []

    controlpoints2 = []  # store control poinst for Bezier
    controlpoints1 = []  # store control poinst for Bezier

    refLength = 0.0

    def __init__(self, name, inports: List[Tuple[float,float,float,float]], splitshift: Tuple[float, float] , *, layer=10):
        OptCell.__init__(self, name, layer)
        self.pathnodes1 = []
        self.pathnodes2 = []
        if isinstance(inports, list):
            self.inports = inports[0:1]
        else:
            self.inports = [inports]

        shift = splitshift

        # calculate outports
        (x, y, dx, dy) = self.inports[0]
        tmpl = 1.0 / np.sqrt(dx * dx + dy * dy)
        dx *= tmpl
        dy *= tmpl
        nx = dy
        ny = -dx
        L, W = shift
        x1 = x + L * dx + 0.5 * W * nx
        y1 = y + L * dy + 0.5 * W * ny
        x2 = x + L * dx - 0.5 * W * nx
        y2 = y + L * dy - 0.5 * W * ny
        self.outports = [(x1, y1, dx, dy), (x2, y2, dx, dy)]

        # generate real control points list 1
        self.refLength = 0.0
        cx1 = x + 0.5 * L * dx
        cy1 = y + 0.5 * L * dy
        cx2 = x + 0.75 * L * dx
        cy2 = y + 0.75 * L * dy
        cx3 = x + 0.75 * L * dx + 0.5 * W * nx
        cy3 = y + 0.75 * L * dy + 0.5 * W * ny
        cx4 = x + 1.0 * L * dx + 0.5 * W * nx
        cy4 = y + 1.0 * L * dy + 0.5 * W * ny
        self.controlpoints1 = [(x, y), (cx1, cy1), (cx2, cy2), (cx3, cy3), (cx4, cy4)]

        # generate real control points list 2
        self.refLength = 0.0
        cx1 = x + 0.5 * L * dx
        cy1 = y + 0.5 * L * dy
        cx2 = x + 0.75 * L * dx
        cy2 = y + 0.75 * L * dy
        cx3 = x + 0.75 * L * dx - 0.5 * W * nx
        cy3 = y + 0.75 * L * dy - 0.5 * W * ny
        cx4 = x + 1.0 * L * dx - 0.5 * W * nx
        cy4 = y + 1.0 * L * dy - 0.5 * W * ny
        self.controlpoints2 = [(x, y), (cx1, cy1), (cx2, cy2), (cx3, cy3), (cx4, cy4)]

        lastx = x
        lasty = y
        # calculate reference length for generating points
        for shiftx, shifty in self.controlpoints1:
            self.refLength += np.sqrt((shiftx - lastx) * (shiftx - lastx) + (shifty - lasty) * (shifty - lasty))
            lastx = shiftx
            lasty = shifty

        self.createmask()

    def createmask(self):
        # generate path 1
        nodes1 = np.asfortranarray(np.transpose(self.controlpoints1))
        curve = bezier.curve.Curve.from_nodes(nodes1, )

        segN = int(float(self.refLength) / config.dfOptRes + 5)
        segs = np.linspace(0.0, 1.0, segN)
        nodes1 = curve.evaluate_multi(segs)

        nodes1 = np.transpose(nodes1)
        self.pathnodes1 = nodes1
        wg1 = gdspy.FlexPath(nodes1, width=config.dfoptwgwidth, layer=0)

        # generate path 2
        nodes2 = np.asfortranarray(np.transpose(self.controlpoints2))
        curve = bezier.curve.Curve.from_nodes(nodes2, )

        segN = int(float(self.refLength) / config.dfOptRes + 5)
        segs = np.linspace(0.0, 1.0, segN)
        nodes2 = curve.evaluate_multi(segs)

        nodes2 = np.transpose(nodes2)
        self.pathnodes2 = nodes2
        wg2 = gdspy.FlexPath(nodes2, width=config.dfoptwgwidth, layer=0)

        # boolean and merge two path
        wgs = gdspy.boolean(wg1,wg2, "or", precision=0.01, layer=self.layer, max_points=config.MAXPOINTS)
        self.add(wgs)

        return None
    #end of OPTYsplitter


class OptYmerger(OptCell):
    """
    Y-Merge waveguide.

    **shift** defines the length the Y merger in the direction of **inports[0]**.

    Args:
        name: str
        inports: List[Tuple[float,float,float,float]]
        shift: float
        layer : int, *default: 10*

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width

    Example
    -------
    >>> wg5 = opthedgehog.OptYsplitter("OptYsplitter", inports=wg4.outports, splitshift=(200.0, 40.0))

    Note
    ----
    The direction of two in ports are assumed to be same; if not, a **warning** message will be printed,
    and only the direction of the first in port (i.e. **inports[0]**) will be used.

    If the two in ports (**inports[0]** and **inports[1]**) are not aligned perpendicular to their directions,
    a **warning** message will be printed and they will be automatically aligned.


    """
    #    OptYmerger, upadated to any angle, and auto align two ports.

    pathnodes1 = []
    pathnodes2 = []

    controlpoints2 = []  # store control poinst for Bezier
    controlpoints1 = []  # store control poinst for Bezier

    refLength: float = 0.0
    realLength: float = 0.0

    def __init__(self, name: str,
                 inports: List[Tuple[float, float, float, float]],
                 shift: float,  # the length of the merger
                 *,
                 layer=10):
        OptCell.__init__(self, name=name, layer=layer)
        self.inports = inports

        if len(self.inports) < 2:
            raise Exception("[optohedgehog] class OptYmerger requires two inports.")

        # calculate outports
        (x1, y1, dx, dy) = self.inports[0]
        (x2, y2, dx2, dy2) = self.inports[1]
        if np.abs(dx * dy2 - dy * dx2) > 1E-10:
            print(colored("[optohedgehog WARNING] class OptYmerger: two inports not parallel, direction of the first port is used", color="blue"))

        Lalign = 0.5 * np.abs((x2 - x1) * dx + (y2 - y1) * dy)
        self.Lalign = Lalign
        if Lalign > 1E-6:
            print(colored(f"[optohedgehog WARNING] class OptYmerger: two inports not aligned, auto aligned, distance {2.0 * Lalign} um", color="blue"))

        tmpl = 1.0 / np.sqrt(dx * dx + dy * dy)
        dx *= tmpl
        dy *= tmpl
        nx = dy
        ny = -dx
        L = shift
        W = (x2 - x1) * nx + (y2 - y1) * ny  # no abs value, to distinguish port 1 and port 2

        x = 0.5 * (x1 + x2) + (L + Lalign) * dx
        y = 0.5 * (y1 + y2) + (L + Lalign) * dy
        self.outports = [(x, y, dx, dy)]

        # merger is reverse of the splitter, reverse (dx, dy)
        dx = -dx
        dy = -dy

        # generate real control points list 1chenged due to updated OptYmerger
        cx1 = x + 0.5 * L * dx
        cy1 = y + 0.5 * L * dy
        cx2 = x + 0.75 * L * dx
        cy2 = y + 0.75 * L * dy
        cx3 = x + 0.75 * L * dx - 0.5 * W * nx
        cy3 = y + 0.75 * L * dy - 0.5 * W * ny
        cx4 = x + 1.0 * L * dx - 0.5 * W * nx
        cy4 = y + 1.0 * L * dy - 0.5 * W * ny
        self.controlpoints1 = [(x, y), (cx1, cy1), (cx2, cy2), (cx3, cy3), (cx4, cy4)]

        # generate real control points list 2
        cx1 = x + 0.5 * L * dx
        cy1 = y + 0.5 * L * dy
        cx2 = x + 0.75 * L * dx
        cy2 = y + 0.75 * L * dy
        cx3 = x + 0.75 * L * dx + 0.5 * W * nx
        cy3 = y + 0.75 * L * dy + 0.5 * W * ny
        cx4 = x + 1.0 * L * dx + 0.5 * W * nx
        cy4 = y + 1.0 * L * dy + 0.5 * W * ny
        self.controlpoints2 = [(x, y), (cx1, cy1), (cx2, cy2), (cx3, cy3), (cx4, cy4)]

        self.refLength = 0.0
        lastx = x
        lasty = y
        # calculate reference length for generating points
        for shiftx, shifty in self.controlpoints1:
            self.refLength += np.sqrt((shiftx - lastx) * (shiftx - lastx) + (shifty - lasty) * (shifty - lasty))
            lastx = shiftx
            lasty = shifty

        self.createmask()

    def createmask(self):
        (x1, y1, dx, dy) = self.inports[0]
        (x2, y2, dx2, dy2) = self.inports[1]

        # generate path 1
        nodes1 = np.asfortranarray(np.transpose(self.controlpoints1))
        curve = bezier.curve.Curve.from_nodes(nodes1, )

        segN = int(float(self.refLength) / config.dfOptRes + 5)
        segs = np.linspace(0.0, 1.0, segN)
        nodes1 = curve.evaluate_multi(segs)

        if self.Lalign > 1E-6:
            nodes1 = np.append(np.transpose(nodes1), [(x1, y1)], axis=0)  # fix the alignment of two ports
        else:
            nodes1 = np.transpose(nodes1)

        self.pathnodes1 = nodes1
        wg1 = gdspy.FlexPath(nodes1, width=config.dfoptwgwidth, layer=0)

        # generate path 2
        nodes2 = np.asfortranarray(np.transpose(self.controlpoints2))
        curve = bezier.curve.Curve.from_nodes(nodes2, )

        segN = int(float(self.refLength) / config.dfOptRes + 5)
        segs = np.linspace(0.0, 1.0, segN)
        nodes2 = curve.evaluate_multi(segs)

        if self.Lalign > 1E-6:
            nodes2 = np.append(np.transpose(nodes2), [(x2, y2)], axis=0)  # fix the alignment of two ports
        else:
            nodes2 = np.transpose(nodes2)

        self.pathnodes2 = nodes2
        wg2 = gdspy.FlexPath(nodes2, width=config.dfoptwgwidth, layer=0)

        # boolean and merge two path
        wgs = gdspy.boolean(wg1, wg2, "or", precision=0.001, layer=self.layer, max_points=config.MAXPOINTS)
        self.add(wgs)

        return None
    #end of OptYmerger


class Opt2x2MMI(OptCell):
    """
    2 x 2 MMI directional coupler
    """
    endwgwidth = 2.0
    MMIwidth = 10.0
    MMIlength = 10.0
    MMIinputoffset = 1.0
    pathnodes1 = []
    pathnodes2 = []
    pathnodes3 = []
    pathnodes4 = []
    MMIstartx = 0
    MMIy = 0


    def __init__(self, name, inports, endwgwidth, MMIwidth, MMIlength, MMIinputoffset, layer=10):
        OptCell.__init__(self, name, layer)
        self.endwgwidth = endwgwidth
        self.MMIwidth = MMIwidth
        self.MMIlength = MMIlength
        self.MMIinputoffset = MMIinputoffset

        if isinstance(inports, list):
            if len(inports) < 2:
                raise ValueError("[OptHedgehog] class Opto2x2MMI: number of IN ports less than two.")
            else:
                self.inports = inports[0:2]
        else:
            raise TypeError("[OptHedgehog] class Opto2x2MMI: request a list of two type.")
        pass

        (x1, y1, dx1, dy1) = self.inports[0]
        (x2, y2, dx2, dy2) = self.inports[1]
        if abs(x1 - x2) > 1e-3:
            warnings.warn("[OptHedgehog WARNING]  merge two optical waveguides with unaligned IN ports: %s" % str(self.inports))
        if y1 < y2:
            warnings.warn("[OptHedgehog WARNING]  In ports swaped. to ensure port 1 y > port2 y, IN ports list: %s" % str(self.inports))
            tmp = self.inports[0]
            self.inports[0] = self.inports[1]
            self.inports[1] = tmp
        if abs(dy1) > 1e-3 or abs(dy2)>1e-3:
            raise ValueError("[OptHedgehog] class Opto2x2MMI: input waveguides has to be horizontal.")

        self.createmask()

    def createmask(self):

        (x1, y1, dx1, dy1) = self.inports[0]
        (x2, y2, dx2, dy2) = self.inports[1]
        #fix
        if abs(x1 - x2) > 1e-3:
            if (x1 < x2):
                wgext1 = gdspy.PolyPath([(x1,y1),(x2,y1)], width=config.dfoptwgwidth, max_points=199, layer=self.layer, corners=1)
                self.add(wgext1)
            else:
                wgext1 = gdspy.PolyPath([(x2, y2), (x1, y2)], width=config.dfoptwgwidth, max_points=199, layer=self.layer, corners=1)
                self.add(wgext1)

        xstart = max(x1, x2)
        ymid = (y1 + y2)/2.0
        upperyend = ymid + self.MMIinputoffset
        loweryend = ymid - self.MMIinputoffset

        ## input wg path1
        px = [x1, x1+config.dfTurningRadius, x1+3.0*config.dfTurningRadius, x1+4.0*config.dfTurningRadius]
        py = [y1, y1, upperyend, upperyend]

        nodes = np.asfortranarray([
            px,
            py,
        ])
        curve = bezier.curve.Curve.from_nodes(nodes, )

        dist = abs(y1-upperyend) + 3.14*4.0*config.dfTurningRadius
        segN = int(float(dist) / 0.16 + 5)

        segs = np.linspace(0.0, 1.0, segN)
        nodes = curve.evaluate_multi(segs)

        nodes = np.transpose(nodes)
        self.pathnodes1 = nodes
        wg1connect = gdspy.PolyPath(nodes, width=config.dfoptwgwidth, max_points=199, layer=self.layer, corners=1)
        wg1expend= gdspy.PolyPath( [(x1+4.0*config.dfTurningRadius,upperyend), (x1+4.0*config.dfTurningRadius+10,upperyend) ],
                                   width = [config.dfoptwgwidth, self.endwgwidth], max_points=199, layer=self.layer, corners=1)

        self.add([wg1connect,wg1expend])


        ## input wg path2
        px = [x2, x2+config.dfTurningRadius, x2+3.0*config.dfTurningRadius, x2+4.0*config.dfTurningRadius]
        py = [y2, y2, loweryend, loweryend]

        nodes = np.asfortranarray([
            px,
            py,
        ])
        curve = bezier.curve.Curve.from_nodes(nodes, )

        dist = abs(y2-loweryend) + 3.14*4.0*config.dfTurningRadius
        segN = int(float(dist) / 0.16 + 5)

        segs = np.linspace(0.0, 1.0, segN)
        nodes = curve.evaluate_multi(segs)

        nodes = np.transpose(nodes)
        self.pathnodes2 = nodes
        wg2connect = gdspy.PolyPath(nodes, width=config.dfoptwgwidth, max_points=199, layer=self.layer, corners=1)
        wg2expend = gdspy.PolyPath([(x2 + 4.0 * config.dfTurningRadius, loweryend), (x2 + 4.0 * config.dfTurningRadius + 10.0, loweryend)],
                                   width=[config.dfoptwgwidth, self.endwgwidth], max_points=199, layer=self.layer, corners=1)
        self.add([wg2connect,wg2expend])

        ########################  MMI ##########
        self.MMIstartx = x2 + 4.0 * config.dfTurningRadius
        self.MMIy = ymid
        MMIstartx = x2 + 4.0 * config.dfTurningRadius + 10.0
        MMIy = ymid
        wgmmi = gdspy.PolyPath([(MMIstartx, MMIy), (MMIstartx + self.MMIlength, MMIy)],
                                   width=self.MMIwidth, max_points=199, layer=self.layer, corners=1)
        self.add(wgmmi)

        ######################   upper output 1 ################
        xout = MMIstartx + self.MMIlength
        wg3expend = gdspy.PolyPath([(xout, loweryend), (xout + 10.0, loweryend)],
                                   width=[self.endwgwidth, config.dfoptwgwidth], max_points=199, layer=self.layer, corners=1)

        xout += 10.0
        px = [xout, xout + config.dfTurningRadius, xout + 3.0 * config.dfTurningRadius, xout + 4.0 * config.dfTurningRadius]
        py = [loweryend, loweryend, y2, y2]
        xout -= 10.0

        nodes = np.asfortranarray([
            px,
            py,
        ])
        curve = bezier.curve.Curve.from_nodes(nodes, )

        dist = abs(y1 - upperyend) + 3.14 * 4.0 * config.dfTurningRadius
        segN = int(float(dist) / 0.16 + 5)

        segs = np.linspace(0.0, 1.0, segN)
        nodes = curve.evaluate_multi(segs)

        nodes = np.transpose(nodes)
        self.pathnodes3 = nodes
        wg3connect = gdspy.PolyPath(nodes, width=config.dfoptwgwidth, max_points=199, layer=self.layer, corners=1)

        self.add([wg3expend, wg3connect])

        ##### lower output
        xout = MMIstartx + self.MMIlength
        wg4expend = gdspy.PolyPath([(xout, upperyend), (xout + 10.0, upperyend)],
                                   width=[self.endwgwidth, config.dfoptwgwidth], max_points=199, layer=self.layer, corners=1)

        xout += 10.0
        px = [xout, xout + config.dfTurningRadius, xout + 3.0 * config.dfTurningRadius, xout + 4.0 * config.dfTurningRadius]
        py = [upperyend, upperyend, y1, y1]
        xout -= 10.0

        nodes = np.asfortranarray([
            px,
            py,
        ])
        curve = bezier.curve.Curve.from_nodes(nodes, )

        dist = abs(y1 - upperyend) + 3.14 * 4.0 * config.dfTurningRadius
        segN = int(float(dist) / 0.16 + 5)

        segs = np.linspace(0.0, 1.0, segN)
        nodes = curve.evaluate_multi(segs)

        nodes = np.transpose(nodes)
        self.pathnodes4 = nodes
        wg4connect = gdspy.PolyPath(nodes, width=config.dfoptwgwidth, max_points=199, layer=self.layer, corners=1)

        self.add([wg4expend, wg4connect])

        ###define output ports
        self.outports=[(xout + 4.0 * config.dfTurningRadius + 10, y1,1.0,0),(xout + 4.0 * config.dfTurningRadius + 10, y2,1.0,0)]


class OptWaveguideCoupler(OptCell):
    """
    Coupling waveguides, 2 inputs X 2 outputs.

    The bending waveguides are of Bezier Curve.

    Args:
        name: str
        inports: List[Tuple[float, float, float, float]]
        taperLength: float -- The length of the bending waveguide from the ports to the coupling region.
        couplingLength: float -- The length of coupling region.
        couplingGap: float -- The gap between two coupling waveguides.
        layer: int, default *10*

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width

    Example:
        >>> couplingWG = opthedgehog.OptWaveguideCoupler("OptWaveguideCoupler", inports=[*wg1.outports, *wg1b.outports], taperLength=100.0, couplingLength=20.0, couplingGap=0.5)


    Note
    ----
    Similar to **OptYmerger**,
    the direction of two in ports are assumed to be same; if not, a **warning** message will be printed,
    and only the direction of the first in port (i.e. **inports[0]**) will be used.

    If the two in ports (**inports[0]** and **inports[1]**) are not aligned perpendicular to their directions,
    a **warning** message will be printed and they will be automatically aligned.
    """
    pathnodes1 = []
    pathnodes2 = []

    controlpoints2 = []  # store control poinst for Bezier
    controlpoints2B = []  # store control poinst for Bezier
    controlpoints1 = []  # store control poinst for Bezier
    controlpoints1B = []  # store control poinst for Bezier

    taperLength = 0.0
    couplingLength = 0.0
    couplingGap = 0.0

    refLength: float = 0.0
    realLength: float = 0.0

    def __init__(self, name: str,
                 inports: List[Tuple[float, float, float, float]],
                 taperLength: float,  # the length of the taper
                 couplingLength: float, # the length of coupling region
                 couplingGap: float,
                 *,
                 layer=10):
        OptCell.__init__(self, name=name, layer=layer)
        self.inports = inports

        if len(self.inports) < 2:
            raise Exception("[optohedgehog] class OptWaveguideCoupler requires two inports.")

        self.taperLength = taperLength
        self.couplingLength = couplingLength
        self.couplingGap = couplingGap

        # calculate outports
        (x1, y1, dx, dy) = self.inports[0]
        (x2, y2, dx2, dy2) = self.inports[1]
        if np.abs(dx * dy2 - dy * dx2) > 1E-10:
            print(colored("[optohedgehog WARNING] class OptYmerger: two inports not parallel, direction of the first port is used", color="blue"))

        Lalign = 0.5 * np.abs((x2 - x1) * dx + (y2 - y1) * dy)
        self.Lalign = Lalign
        if Lalign > 1E-6:
            print(colored(f"[optohedgehog WARNING] class OptYmerger: two inports not aligned, auto aligned, distance {2.0 * Lalign} um", color="blue"))

        tmpl = 1.0 / np.sqrt(dx * dx + dy * dy)
        dx *= tmpl
        dy *= tmpl
        nx = dy
        ny = -dx
        L = self.taperLength
        W = (x2 - x1) * nx + (y2 - y1) * ny  # no abs value, to distinguish port 1 and port 2
        G = np.sign(W) * (self.couplingGap + config.dfoptwgwidth) # coupling gap, keep the order
        if abs(G) < 1E-6:   # in the special case W == 0
            G = self.couplingGap + config.dfoptwgwidth


        #coordinate of the merged point
        x = 0.5 * (x1 + x2) + (L + Lalign) * dx
        y = 0.5 * (y1 + y2) + (L + Lalign) * dy
        x1out = x + (L+self.couplingLength) * dx - 0.5 * W * nx
        y1out = y + (L + self.couplingLength) * dy - 0.5* W * ny
        x2out = x + (L + self.couplingLength) * dx + 0.5 * W * nx
        y2out = y + (L + self.couplingLength) * dy + 0.5 * W * ny
        self.outports = [(x1out, y1out, dx, dy), (x2out, y2out, dx, dy)]

        # merger is reverse of the splitter, reverse (dx, dy)
        dx = -dx
        dy = -dy


        # generate real control points list, port 1 merging part
        cx1 = x + 0.0 * L * dx - 0.5 * G * nx
        cy1 = y + 0.0 * L * dy - 0.5 * G * ny
        cx2 = x + 0.3 * L * dx - 0.5 * G * nx
        cy2 = y + 0.3 * L * dy - 0.5 * G * ny
        cx3 = x + 0.5 * L * dx - 0.5 * W * nx
        cy3 = y + 0.5 * L * dy - 0.5 * W * ny
        cx4 = x + 1.0 * L * dx - 0.5 * W * nx
        cy4 = y + 1.0 * L * dy - 0.5 * W * ny
        self.controlpoints1 = [(cx1, cy1), (cx2, cy2), (cx3, cy3), (cx4, cy4)]

        # generate real control points list 2
        cx1 = x + 0.0 * L * dx + 0.5 * G * nx
        cy1 = y + 0.0 * L * dy + 0.5 * G * ny
        cx2 = x + 0.3 * L * dx + 0.5 * G * nx
        cy2 = y + 0.3 * L * dy + 0.5 * G * ny
        cx3 = x + 0.5 * L * dx + 0.5 * W * nx
        cy3 = y + 0.5 * L * dy + 0.5 * W * ny
        cx4 = x + 1.0 * L * dx + 0.5 * W * nx
        cy4 = y + 1.0 * L * dy + 0.5 * W * ny
        self.controlpoints2 = [(cx1, cy1), (cx2, cy2), (cx3, cy3), (cx4, cy4)]

        self.refLength = 0.0
        lastx = x
        lasty = y
        # calculate reference length for generating points
        for shiftx, shifty in self.controlpoints1:
            self.refLength += np.sqrt((shiftx - lastx) * (shiftx - lastx) + (shifty - lasty) * (shifty - lasty))
            lastx = shiftx
            lasty = shifty


        #seperate apart part
        dx *= -1.0
        dy *= -1.0
        x += self.couplingLength * dx
        y += self.couplingLength * dy
        # generate real control points list, port 1 apart part
        cx1 = x + 0.0 * L * dx - 0.5 * G * nx
        cy1 = y + 0.0 * L * dy - 0.5 * G * ny
        cx2 = x + 0.3 * L * dx - 0.5 * G * nx
        cy2 = y + 0.3 * L * dy - 0.5 * G * ny
        cx3 = x + 0.5 * L * dx - 0.5 * W * nx
        cy3 = y + 0.5 * L * dy - 0.5 * W * ny
        cx4 = x + 1.0 * L * dx - 0.5 * W * nx
        cy4 = y + 1.0 * L * dy - 0.5 * W * ny
        self.controlpoints1B = [(cx1, cy1), (cx2, cy2), (cx3, cy3), (cx4, cy4)]

        #generate apart port 2
        cx1 = x + 0.0 * L * dx + 0.5 * G * nx
        cy1 = y + 0.0 * L * dy + 0.5 * G * ny
        cx2 = x + 0.3 * L * dx + 0.5 * G * nx
        cy2 = y + 0.3 * L * dy + 0.5 * G * ny
        cx3 = x + 0.5 * L * dx + 0.5 * W * nx
        cy3 = y + 0.5 * L * dy + 0.5 * W * ny
        cx4 = x + 1.0 * L * dx + 0.5 * W * nx
        cy4 = y + 1.0 * L * dy + 0.5 * W * ny
        self.controlpoints2B = [(cx1, cy1), (cx2, cy2), (cx3, cy3), (cx4, cy4)]


        self.createmask()

    def createmask(self):
        (x1, y1, dx, dy) = self.inports[0]
        (x2, y2, dx2, dy2) = self.inports[1]

        # generate path 1
        nodes1 = _genBezierPath(self.controlpoints1)
        if self.Lalign > 1E-6:
            nodes1 = np.append(nodes1, [(x1, y1)], axis=0)  # fix the alignment of two ports
        nodes1 = np.flip(nodes1, axis=0)

        #apart part
        nodes1B = _genBezierPath(self.controlpoints1B)

        self.pathnodes1 = [*nodes1, *nodes1B]
        wg1 = gdspy.FlexPath(self.pathnodes1, width=config.dfoptwgwidth, layer=self.layer, max_points=config.MAXPOINTS)

        # generate path 2
        nodes2 = _genBezierPath(self.controlpoints2)
        if self.Lalign > 1E-6:
            nodes2 = np.append(nodes2, [(x2, y2)], axis=0)  # fix the alignment of two ports
        nodes2 = np.flip(nodes2, axis = 0)

        #apart part
        nodes2B = _genBezierPath(self.controlpoints2B)

        self.pathnodes2 = [*nodes2, *nodes2B]
        wg2 = gdspy.FlexPath(self.pathnodes2, width=config.dfoptwgwidth, layer=self.layer, max_points=config.MAXPOINTS)

        #add both path
        self.add([wg1, wg2])

        return None
    # end of OptWaveguideCoupler


class OptAddOnWaveguideCoupler(OptCell):
    """
    Add a coupling waveguide to an exsiting waveguide.

    Args:
        name: str
        inports: List[Tuple[float, float, float, float]]
        couplingPos: List[Tuple[float, float, float, float]] -- The position of the coupling on the existing waveguide.
        couplingLength: float -- The length of coupling region.
        couplingPitch: float -- In the coupling region, the distance between the center line of the two waveguides.
        layer: int, default *10*

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width

    Example:
        >>> #Define two exsiting waveguides, and add a coupling waveguide at their joint.
        >>> wgCpl1 = opthedgehog.OptStraightWaveguide("OptStraightWaveguide", inports=[(-1000, 300, 1.0, 0.0)], length=500, layer = 1)
        >>> wgCpl2 = opthedgehog.OptStraightWaveguide("OptStraightWaveguide", inports=wgCpl1.outports, length=500, layer=2)
        >>> #Add the coupling waveguide
        >>> wgCplA = opthedgehog.OptAddOnWaveguideCoupler("OptAddOnWaveguideCoupler", inports=[(-800, 350, 1. , 0.0)], couplingPos=wgCpl1.outports, couplingLength=50., couplingPitch=2.0, layer = 3)


    """
    pathnodes = []

    cplPos = (0., 0., 0., 0.)
    cplPitch = 0.0
    cplLen = 0.0
    refTR = 0.0

    magic = 0.6 #for path curve control

    def __init__(self, name: str,
                 inports: List[Tuple[float, float, float, float]],
                 couplingPos: List[Tuple[float, float, float, float]],
                 couplingLength: float, # the length of coupling region
                 couplingPitch: float,
                 *,
                 layer=10,
                 curveParameter:float = -1.):
        OptCell.__init__(self, name=name, layer=layer)
        self.inports = inports

        self.cplPos = couplingPos
        self.cplLen = couplingLength
        self.cplPitch = couplingPitch

        if curveParameter > 0:
            self.magic = curveParameter

        #calculate outport ports in createMask()

        self.createMask()

    def createMask(self):

        #inports
        (xin, yin, dxin, dyin) = self.inports[0]
        dxin, dyin = _normalizedxdy(dxin, dyin)
        (xc, yc, dxc, dyc) = self.cplPos[0]
        dxc, dyc = _normalizedxdy(dxc, dyc)


        #shiftcoupling pitch

        # get the position left/right of the Xin, Yin
        nxc, nyc = -dyc , dxc
        dir = np.sign( (xin-xc) * nxc + (yin-yc) * nyc)
        if 0 == dir:
            dir = 1
        nxc *= dir
        nyc *= dir
        #shift the coupling position
        xc += self.cplPitch * nxc
        yc += self.cplPitch * nyc

        #approaching coupling waveguide
        extl1 = self.magic*np.abs((xc-xin) * dxin + (yc-yin) * dyin)
        ctrP1 = (xin + extl1 * dxin,  yin + extl1 * dyin )

        extl2 = self.magic*0.8 * np.abs((xc - xin) * dxc + (yc - yin) * dyc)
        ctrP2 = (xc - extl2 * dxc,  yc - extl2 * dyc)

        cplinwg = [(xin, yin), ctrP1, ctrP2, (xc, yc)]

        ptswg1 = _genBezierPath(cplinwg)

        #coupling length
        xce = xc + self.cplLen * dxc
        yce = yc + self.cplLen * dyc

        #calculate the output port #symmetric Coupler
        d1 = 2.*(xc-xin) * dxc + 2. * (yc-yin) * dyc + self.cplLen
        # print(f"{d1=}")
        xout = xin + d1 * dxc
        yout = yin + d1 * dyc
        # print(f" [ DEBUG ]   {xin, yin = }")
        # print(f" [ DEBUG ]   {xout, yout = }")

        prallel = dxin * dxc + dyin * dyc
        prep = dxin * nxc + dyin * nyc
        dxout = prallel * dxc - prep * nxc
        dyout = prallel * dyc - prep * nyc
        self.outports = [(xout, yout, dxout, dyout)]


        ctrP3 = (xce + extl2 * dxc, yce + extl2 * dyc)
        ctrP4 = (xout - extl1 * dxout, yout - extl1*dyout)
        cplinwg2 = [(xce, yce), ctrP3, ctrP4, (xout, yout)]

        ptswg2 = _genBezierPath(cplinwg2)

        if self.cplLen < 1e-6:
            ptswg = [ *ptswg1, *ptswg2[1:] ]
        else:
            ptswg = [*ptswg1, *ptswg2]

        self.pathnodes = ptswg

        wg1 = gdspy.FlexPath(ptswg, config.dfoptwgwidth, layer = self.layer, max_points=config.MAXPOINTS)
        self.add(wg1)

        pass
    # end of OptAddOnWavegiodeCoupler


class OptRingCavity(OptCell):
    """
    Circulator ring resonator

    Args:
        name: str
        inports: List[Tuple[float, float, float, float]]
        cavityradius:float
        couplinggap:float
        ringwidth: float, default *-1.0* means using the same width as the coupling waveguide,
        layer: int, default 10,
        direction: int, default *1* -- 1 or -1, 1 (-1) indicates the ring is on the left (right) of the waveguide referenced to the input port.
        PlotCouplingWG: bool default *True* -- if *False*, the coupling waveguide won't be plotted.

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width

    Example:
        >>> cavity2 = opthedgehog.OptRingCavity("OptRingCavity", inports=wg5.outports, cavityradius=50.0, couplinggap=2.0, direction=-1, layer = 2)


    """
    xcenter = 0.0
    ycenter = 0.0
    cavityradius = 0.0
    couplinggap = 0.0
    direction = -1
    ringwidth = 0.0
    couplingWG = True

    def __init__(self, name: str, inports: List[Tuple[float, float, float, float]],
                 cavityradius:float, couplinggap:float,
                 *, ringwidth= -1.0, layer:int =10, direction:int =1, PlotCouplingWG: bool = True):
        OptCell.__init__(self, name, layer)
        if isinstance(inports, list):
            self.inports = inports[0:1]
        else:
            self.inports = [inports]

        self.direction = direction
        self.couplingWG = PlotCouplingWG

        if ringwidth < -0.5:
            self.ringwidth = config.dfoptwgwidth
        else:
            self.ringwidth = ringwidth

        (x, y, dx, dy) = self.inports[0]
        dx, dy = _normalizedxdy(dx, dy)
        self.inports[0] = (x, y, dx, dy)

        length = 2 * cavityradius
        self.outports = [(x + dx*length, y + dy*length, dx, dy)]
        self.cavityradius = cavityradius
        self.couplinggap = couplinggap
        self.createmask()

        #end of __init___

    def createmask(self):
        (x0, y0, dx, dy) = self.inports[0]
        (xend, yend, tmp, tmp) = self.outports[0]

        #normal direction (right hand)
        dxn = -dy
        dyn = dx

        offset = (self.cavityradius + config.dfoptwgwidth/2.0 + self.ringwidth/2.0 + self.couplinggap) * self.direction
        xcut = x0 + self.cavityradius * dx +  offset * dxn
        ycut = y0 + self.cavityradius * dy +  offset * dyn
        self.xcenter = xcut
        self.ycenter = ycut

        # add optical waveguide
        if self.couplingWG:
            wg1 = gdspy.FlexPath(points=[(x0, y0), (xend, yend)], width=config.dfoptwgwidth, layer=self.layer)
            self.add(wg1)

        # add optical ring cavity
        cavity1 = gdspy.Round((self.xcenter, self.ycenter),
                              radius=self.cavityradius + self.ringwidth / 2,
                              inner_radius=self.cavityradius - self.ringwidth / 2,
                              number_of_points= int(4*np.pi*self.cavityradius / config.dfOptRes + 5),
                              layer=self.layer,
                              max_points=config.MAXPOINTS)
        self.add(cavity1)

        #add ebeam filed guide
        t = (self.ringwidth + self.couplinggap + config.dfoptwgwidth)*2.0
        guide = gdspy.Rectangle((self.xcenter - self.cavityradius - t, self.ycenter - self.cavityradius - t),
                                (self.xcenter + self.cavityradius + t, self.ycenter + self.cavityradius + t), layer=0)
        self.add(guide)

        return None

    #end of OptRingCavity


class OptDiskCavity(OptCell):
    """
    Circulator Disk resonator

    Args:
        name: str
        inports: List[Tuple[float, float, float, float]]
        cavityradius:float
        couplinggap:float
        layer: int, default 10,
        direction: int, default *1* -- 1 or -1, 1 (-1) indicates the ring is on the left (right) of the waveguide referenced to the input port.
        PlotCouplingWG: bool default *True* -- if *False*, the coupling waveguide won't be plotted.

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width

    Example:
        >>> cavity5 = opthedgehog.OptDiskCavity("OptDiskCavity", inports=wg8.outports, cavityradius=50.0, couplinggap=2.0, direction=1, layer=2)


    """
    xcenter = 0.0
    ycenter = 0.0
    cavityradius = 0.0
    couplinggap = 0.0
    direction = -1
    # ringwidth = 0.0
    couplingWG = True

    def __init__(self, name: str, inports: List[Tuple[float, float, float, float]],
                 cavityradius:float, couplinggap:float,
                 *, layer:int =10, direction:int =1, PlotCouplingWG: bool = True):
        OptCell.__init__(self, name, layer)
        if isinstance(inports, list):
            self.inports = inports[0:1]
        else:
            self.inports = [inports]

        self.direction = direction
        self.couplingWG = PlotCouplingWG

        (x, y, dx, dy) = self.inports[0]
        dx, dy = _normalizedxdy(dx, dy)
        self.inports[0] = (x, y, dx, dy)

        length = 2 * cavityradius
        self.outports = [(x + dx*length, y + dy*length, dx, dy)]
        self.cavityradius = cavityradius
        self.couplinggap = couplinggap
        self.createmask()

        #end of __init___

    def createmask(self):
        (x0, y0, dx, dy) = self.inports[0]
        (xend, yend, tmp, tmp) = self.outports[0]

        #normal direction (right hand)
        dxn = -dy
        dyn = dx

        offset = (self.cavityradius + config.dfoptwgwidth/2.0 + self.couplinggap) * self.direction
        xcut = x0 + self.cavityradius * dx +  offset * dxn
        ycut = y0 + self.cavityradius * dy +  offset * dyn
        self.xcenter = xcut
        self.ycenter = ycut

        # add optical waveguide
        if self.couplingWG:
            wg1 = gdspy.FlexPath(points=[(x0, y0), (xend, yend)], width=config.dfoptwgwidth, layer=self.layer)
            self.add(wg1)

        # add optical ring cavity
        cavity1 = gdspy.Round((self.xcenter, self.ycenter),
                              radius=self.cavityradius,
                              inner_radius=0,
                              number_of_points= int(4*np.pi*self.cavityradius / config.dfOptRes + 5),
                              layer=self.layer,
                              max_points=config.MAXPOINTS)
        self.add(cavity1)

        #add ebeam filed guide
        t = (self.couplinggap + config.dfoptwgwidth + 3.)*2.0
        guide = gdspy.Rectangle((self.xcenter - self.cavityradius - t, self.ycenter - self.cavityradius - t),
                                (self.xcenter + self.cavityradius + t, self.ycenter + self.cavityradius + t), layer=0)
        self.add(guide)

        return None

    #end of OptDiskCavity



class OptRaceTrackCavity(OptCell):
    """
    Optical Race Track cavity.

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

    Global Parameters:
        * config.dfoptwgwidth: Waveguide width
        * config.dfOptRes: control resolution of the curves in micron, recommend and default 0.3

    Example:
        >>> cavityR3 = opthedgehog.OptRaceTrackCavity("OptRaceTrackCavity", inports=wg6.outports, cavityCornerRadius=50.0, cavityLength=200.0, cavityWidth=0.0, couplinggap=1.0, layer = 2)


    """
    xcenter = 0.0
    ycenter = 0.0

    cavityCornerRadius = 0.0
    cavityLength = 0.0
    cavityWidth = 0.0

    couplinggap = 0.0
    direction = -1
    ringwidth = 0.0
    couplingWG = True

    pathnodes = []

    def __init__(self, name: str, inports: List[Tuple[float, float, float, float]],
                 cavityCornerRadius: float, cavityLength: float, cavityWidth:float , couplinggap: float,
                 *, ringwidth=-1.0, layer=10, direction=1, PlotCouplingWG = True):
        OptCell.__init__(self, name, layer)
        if isinstance(inports, list):
            self.inports = inports[0:1]
        else:
            self.inports = [inports]

        self.direction = direction
        self.couplingWG = PlotCouplingWG

        if ringwidth < -0.5:
            self.ringwidth = config.dfoptwgwidth
        else:
            self.ringwidth = ringwidth

        (x, y, dx, dy) = self.inports[0]
        dx, dy = _normalizedxdy(dx, dy)
        self.inports[0] = (x, y, dx, dy)

        length = 2 * cavityCornerRadius + cavityWidth
        self.outports = [(x + dx * length, y + dy * length, dx, dy)]

        self.cavityCornerRadius = cavityCornerRadius
        self.cavityLength = cavityLength
        self.cavityWidth = cavityWidth

        self.couplinggap = couplinggap
        self.createmask()

        # end of __init___

    def createmask(self):
        (x0, y0, dx, dy) = self.inports[0]
        (xend, yend, tmp, tmp) = self.outports[0]

        # normal direction (right hand)

        dxn = -dy*self.direction
        dyn = dx*self.direction
        # print(f"DEBUG: {self.direction=}")
        # print(f"DEBUG: {dxn=}")
        # print(f"DEBUG: {dyn=}")

        offset = (self.cavityCornerRadius + self.cavityLength/2.0 + config.dfoptwgwidth / 2.0 + self.ringwidth / 2.0 + self.couplinggap)
        length = 2 * self.cavityCornerRadius + self.cavityWidth
        xcut = x0 + 0.5*length * dx + offset * dxn
        ycut = y0 + 0.5*length * dy + offset * dyn
        self.xcenter = xcut
        self.ycenter = ycut

        # add optical waveguide
        if self.couplingWG:
            wg1 = gdspy.FlexPath(points=[(x0, y0), (xend, yend)], width=config.dfoptwgwidth, layer=self.layer)
            self.add(wg1)


        #add race track cavity
        cp1 = [ (xcut + (-self.cavityWidth/2.0 - self.cavityCornerRadius) * dx + (-self.cavityLength/2.0) * dxn,
                       ycut + (-self.cavityWidth/2.0 - self.cavityCornerRadius) * dy + (-self.cavityLength/2.0) * dyn),
                (xcut + (-self.cavityWidth/2.0 - self.cavityCornerRadius) * dx + (-self.cavityLength/2.0 - self.cavityCornerRadius) * dxn,
                       ycut + (-self.cavityWidth/2.0 - self.cavityCornerRadius) * dy + (-self.cavityLength/2.0 - self.cavityCornerRadius) * dyn,),
                (xcut + (-self.cavityWidth/2.0 )                          * dx + (-self.cavityLength/2.0 - self.cavityCornerRadius) * dxn,
                       ycut + (-self.cavityWidth/2.0 )                          * dy + (-self.cavityLength/2.0 - self.cavityCornerRadius) * dyn),
                ]
        nodes1 = _genBezierPath(cp1)

        cp2 = [ (xcut + (+self.cavityWidth/2.0) * dx + (-self.cavityLength/2.0 - self.cavityCornerRadius) * dxn,
                       ycut + (+self.cavityWidth/2.0) * dy + (-self.cavityLength/2.0 - self.cavityCornerRadius) * dyn),
                (xcut + (+self.cavityWidth/2.0 + self.cavityCornerRadius) * dx + (-self.cavityLength/2.0 - self.cavityCornerRadius) * dxn,
                       ycut + (+self.cavityWidth/2.0 + self.cavityCornerRadius) * dy + (-self.cavityLength/2.0 - self.cavityCornerRadius) * dyn,),
                (xcut + (+self.cavityWidth/2.0 + self.cavityCornerRadius) * dx + (-self.cavityLength/2.0 ) * dxn,
                       ycut + (+self.cavityWidth/2.0 + self.cavityCornerRadius ) * dy + (-self.cavityLength/2.0 ) * dyn),
                ]
        nodes2 = _genBezierPath(cp2)

        cp3 = [  (xcut + (+self.cavityWidth/2.0 + self.cavityCornerRadius) * dx + (+self.cavityLength/2.0 ) * dxn,
                       ycut + (+self.cavityWidth/2.0 + self.cavityCornerRadius ) * dy + (+self.cavityLength/2.0 ) * dyn),
                 (xcut + (+self.cavityWidth / 2.0 + self.cavityCornerRadius) * dx + (+self.cavityLength / 2.0 + self.cavityCornerRadius) * dxn,
                      ycut + (+self.cavityWidth / 2.0 + self.cavityCornerRadius) * dy + (+self.cavityLength / 2.0 + self.cavityCornerRadius) * dyn),
                 (xcut + (+self.cavityWidth / 2.0 ) * dx + (+self.cavityLength / 2.0 + self.cavityCornerRadius) * dxn,
                      ycut + (+self.cavityWidth / 2.0 ) * dy + (+self.cavityLength / 2.0 + self.cavityCornerRadius) * dyn),
                ]
        nodes3 = _genBezierPath(cp3)

        cp4 = [ (xcut + (-self.cavityWidth / 2.0 ) * dx + (+self.cavityLength / 2.0 + self.cavityCornerRadius) * dxn,
                      ycut + (-self.cavityWidth / 2.0 ) * dy + (+self.cavityLength / 2.0 + self.cavityCornerRadius) * dyn),
                (xcut + (-self.cavityWidth / 2.0 - self.cavityCornerRadius) * dx + (+self.cavityLength / 2.0 + self.cavityCornerRadius) * dxn,
                      ycut + (-self.cavityWidth / 2.0 - self.cavityCornerRadius) * dy + (+self.cavityLength / 2.0 + self.cavityCornerRadius) * dyn),
                (xcut + (-self.cavityWidth / 2.0 - self.cavityCornerRadius) * dx + (+self.cavityLength / 2.0) * dxn,
                      ycut + (-self.cavityWidth / 2.0 - self.cavityCornerRadius) * dy + (+self.cavityLength / 2.0) * dyn),
                ]
        nodes4 = _genBezierPath(cp4)

        self.pathnodes = [*nodes1, *nodes2, *nodes3, *nodes4, nodes1[0]]

        wgcavity = gdspy.FlexPath([*nodes1, *nodes2, *nodes3, *nodes4, nodes1[0]], width=self.ringwidth, layer=self.layer, max_points=config.MAXPOINTS)

        self.add(wgcavity)

        # add ebeam filed guide
        t = self.ringwidth + config.dfoptwgwidth + self.couplinggap
        outboundary = [
            (xcut + (-self.cavityWidth / 2.0 - self.cavityCornerRadius - t*4.0) * dx + (+self.cavityLength / 2.0 + self.cavityCornerRadius + t*4.0) * dxn,
             ycut + (-self.cavityWidth / 2.0 - self.cavityCornerRadius - t*4.0) * dy + (+self.cavityLength / 2.0 + self.cavityCornerRadius + t*4.0) * dyn),

            (xcut + (+self.cavityWidth / 2.0 + self.cavityCornerRadius + t*4.0) * dx + (+self.cavityLength / 2.0 + self.cavityCornerRadius + t*4.0) * dxn,
             ycut + (+self.cavityWidth / 2.0 + self.cavityCornerRadius + t*4.0) * dy + (+self.cavityLength / 2.0 + self.cavityCornerRadius + t*4.0) * dyn),

            (xcut + (+self.cavityWidth / 2.0 + self.cavityCornerRadius + t*4.0) * dx + (-self.cavityLength / 2.0 - self.cavityCornerRadius - t*4.0) * dxn,
             ycut + (+self.cavityWidth / 2.0 + self.cavityCornerRadius + t*4.0) * dy + (-self.cavityLength / 2.0 - self.cavityCornerRadius - t*4.0) * dyn,),

            (xcut + (-self.cavityWidth / 2.0 - self.cavityCornerRadius - t*4.0) * dx + (-self.cavityLength / 2.0 - self.cavityCornerRadius - t*4.0) * dxn,
             ycut + (-self.cavityWidth / 2.0 - self.cavityCornerRadius - t*4.0) * dy + (-self.cavityLength / 2.0 - self.cavityCornerRadius - t*4.0) * dyn,),
        ]
        refbox = gdspy.Polygon(outboundary, layer = 0)
        self.add(refbox)

        return None

    # end of OptRaceTrackCavity


def _normalizedxdy(dx: float, dy: float):
    if dx*dx + dy*dy < 1E-6 :
        raise Exception("[opthedgehog] Direction (dx, dy) is 0.")
    else:
        norm = np.sqrt( np.square(dx)+np.square(dy))
        dx /= norm
        dy /= norm
    return dx, dy


def _genBezierPath(controlpoints: List[Tuple[float, float]]):

    refLength = 0.0
    xlast, ylast = controlpoints[0]
    for x,y in controlpoints[1:]:
        refLength += np.sqrt( (x-xlast)*(x-xlast) + (y-ylast)*(y-ylast) )

    nodes = np.asfortranarray(np.transpose(controlpoints))
    curve = bezier.curve.Curve.from_nodes(nodes, )

    segN = int(float(refLength) / config.dfOptRes + 5)
    segs = np.linspace(0.0, 1.0, segN)
    nodes = curve.evaluate_multi(segs)

    nodes = np.transpose(nodes)

    return nodes
    #end of _genBezierPath


def _taperPath(points: List[Tuple[float, float, ]], width: Union[float, List[float]], layer: int):
    if len(points) < 2:
        Warning("[_opthedgehog] dunc _taperPath, The number of points < 2.")

    l = len(points)
    if isinstance(width, float):
        width = width * np.ones(l)

    first = True
    xlast, ylast, *tmp = points[0]
    wlast = width[0]

    pos = []
    neg = []

    for point, w in zip(points[1:], width[1:]):
        xcut, ycut, *tmp = point

        dx, dy = xcut - xlast, ycut - ylast
        nx, ny = _normalizedxdy(dy , -dx)
        if first:
            pos.append( ( xlast + nx * wlast * 0.5, ylast + ny * wlast * 0.5 ) )
            neg.append( (xlast - nx * wlast * 0.5, ylast - ny * wlast * 0.5) )
            first = False

        pos.append((xcut + nx * w * 0.5, ycut + ny * w * 0.5))
        neg.append((xcut - nx * w * 0.5, ycut - ny * w * 0.5))

        xlast, ylast = xcut, ycut

    if len(pos) > 1:
        neg.reverse()
        pattern = gdspy.Polygon([*pos, *neg], layer = layer)
        return pattern
    else:
        return None

    #end of _taperPath

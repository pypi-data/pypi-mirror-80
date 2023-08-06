######################################################################################
## Author: Linbo Shao
## Date: Jan, 2020
## Copyright 2019-2020 Linbo Shao All Rights Reserved
######################################################################################



from typing import List, Tuple
import gdspy
import warnings
from termcolor import colored
import numpy as np
import bezier

from . import config
from .optCells import OptCell

class AcousticStraightWaveguide(OptCell):
    """
    Acoustic waveguides
    """
    length = 0.0
    def __init__(self,
                 name:str,
                 inports: List[Tuple[float,float,float,float]],
                 length: float,
                 *,
                 layer:int=5,
                 endwidth:float=-1):
        super().__init__(name, layer)
        if isinstance(inports, list):
            self.inports = inports
        else:
            self.inports.append(inports)

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

        #endiwdth
        if endwidth < -0.5:
            self.endwidth = config.dfAcuwgWidth
        else:
            self.endwidth = endwidth
            print( colored(f"[optohedgehog WARNING] tapering acoustic waveguide, the global setting *config.dfAcuwgwidth* changed to {endwidth}.",
                           "blue"))

        self.createMask()

        config.dfAcuwgWidth = self.endwidth

        pass
    # end __init__

    def createMask(self):
        startpos = (self.inports[0][0], self.inports[0][1])
        endpos = (self.outports[0][0],self.outports[0][1])
        path = [startpos, endpos]
        width =[config.dfAcuwgWidth, self.endwidth]
        shape = _createAcousticNegWGmask(path, width, etchlayer=self.layer)
        self.add(shape)

        pass

class AcousticBezierWaveguide(OptCell):
    """
       AcousticBezierWaveguide
    """
    path = []  # store the nodes of the Bezier curve
    controlpoints = []  # store control poinst for Bezier
    refLength :float = 0.0
    realLength :float = 0.0

    def __init__(self, name: str,
                 inports: List[Tuple[float,float,float,float]],
                 controlpoints: List[Tuple[float, float]],  # relative control points for Bezier curve, the inport is added automatically
                 *,
                 layer=5):
        OptCell.__init__(self, name=name, layer=layer)
        if isinstance(inports, list):
            self.inports = inports
        else:
            self.inports = [inports]

        # generate real control points list
        (x, y, dx, dy) = self.inports[0]
        self.refLength = 0.0
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

        self.pathnodes = []

        self.createmask()

    def createmask(self):


        nodes = np.asfortranarray(np.transpose(self.controlpoints))
        curve = bezier.curve.Curve.from_nodes(nodes)

        segN = int(float(self.refLength) / config.dfAcuRes + 5)
        segs = np.linspace(0.0, 1.0, segN)
        nodes = curve.evaluate_multi(segs)

        nodes = np.transpose(nodes)
        self.pathnodes = nodes
        wg = _createAcousticNegWGmask(nodes, width=config.dfAcuwgWidth, etchlayer=self.layer)
        self.add(wg)
        return None
#end of class AcousticBezierWaveguide



class AcousticYSplitter(OptCell):
    """
       AcousticYSplitter
    """
    path2 = []  # store the nodes of the Bezier curve
    path1 = []  # store the nodes of the Bezier curve

    controlpoints2 = []  # store control poinst for Bezier
    controlpoints1 = []  # store control poinst for Bezier

    refLength :float = 0.0
    realLength :float = 0.0

    def __init__(self, name: str,
                 inports: List[Tuple[float,float,float,float]],
                 shift: Tuple[float, float],  #size for the Y splitter
                 *,
                 layer=5,
                 endwidth = -1):
        OptCell.__init__(self, name=name, layer=layer)
        if isinstance(inports, list):
            self.inports = inports
        else:
            self.inports = [inports]

        #calculate outports
        (x, y, dx, dy) = self.inports[0]
        tmpl = 1.0/np.sqrt(dx*dx + dy*dy)
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
        cx1 = x + 0.3 * L * dx
        cy1 = y + 0.3 * L * dy
        cx2 = x + 0.6 * L * dx
        cy2 = y + 0.6 * L * dy
        cx3 = x + 0.6 * L * dx + 0.5 * W * nx
        cy3 = y + 0.6 * L * dy + 0.5 * W * ny
        cx4 = x + 1.0 * L * dx + 0.5 * W * nx
        cy4 = y + 1.0 * L * dy + 0.5 * W * ny
        self.controlpoints1 = [ (x,y), (cx1, cy1), (cx2, cy2),(cx3, cy3),(cx4, cy4) ]

        # generate real control points list 2
        self.refLength = 0.0
        cx1 = x + 0.3 * L * dx
        cy1 = y + 0.3 * L * dy
        cx2 = x + 0.6 * L * dx
        cy2 = y + 0.6 * L * dy
        cx3 = x + 0.6 * L * dx - 0.5 * W * nx
        cy3 = y + 0.6 * L * dy - 0.5 * W * ny
        cx4 = x + 1.0 * L * dx - 0.5 * W * nx
        cy4 = y + 1.0 * L * dy - 0.5 * W * ny
        self.controlpoints2 = [ (x,y), (cx1, cy1), (cx2, cy2),(cx3, cy3),(cx4, cy4) ]


        lastx = x
        lasty = y
        #calculate reference length for generating points
        for shiftx, shifty in self.controlpoints1:
            self.refLength += np.sqrt((shiftx-lastx)*(shiftx-lastx) + (shifty-lasty)*(shifty-lasty))
            lastx = shiftx
            lasty = shifty



        self.createmask()

    def createmask(self):
        #generate path 1
        nodes1 = np.asfortranarray(np.transpose(self.controlpoints1))
        curve = bezier.curve.Curve.from_nodes(nodes1)

        segN = int(float(self.refLength) / config.dfAcuRes + 5)
        segs = np.linspace(0.0, 1.0, segN)
        nodes1 = curve.evaluate_multi(segs)

        nodes1 = np.transpose(nodes1)
        self.path1 = nodes1
        wg1out, wg1in = _createAcousticNegWGmask(nodes1, width=config.dfAcuwgWidth, etchlayer=0, beforeBool=True)

        #generate path 2
        nodes2 = np.asfortranarray(np.transpose(self.controlpoints2))
        curve = bezier.curve.Curve.from_nodes(nodes2)

        segN = int(float(self.refLength) / config.dfAcuRes + 5)
        segs = np.linspace(0.0, 1.0, segN)
        nodes2 = curve.evaluate_multi(segs)

        nodes2 = np.transpose(nodes2)
        self.path2 = nodes2
        wg2out, wg2in = _createAcousticNegWGmask(nodes2, width=config.dfAcuwgWidth, etchlayer=0, beforeBool=True)

        #boolean and merge two path
        wgs = gdspy.boolean([wg1out,wg2out],[wg1in,wg2in], "not", precision=0.01, layer=self.layer, max_points=config.MAXPOINTS)
        self.add(wgs)

        return None
#end of class AcousticYSplitter


class AcousticYMerger(OptCell):
    """
       AcousticYMerger
    """
    path2 = []  # store the nodes of the Bezier curve
    path1 = []  # store the nodes of the Bezier curve

    controlpoints2 = []  # store control poinst for Bezier
    controlpoints1 = []  # store control poinst for Bezier

    refLength :float = 0.0
    realLength :float = 0.0

    def __init__(self, name: str,
                 inports: List[Tuple[float,float,float,float]],
                 shift: float,  #the length of the merger
                 *,
                 layer=5):
        OptCell.__init__(self, name=name, layer=layer)
        self.inports = inports

        if len(self.inports)<2:
            raise Exception("[optohedgehog] class AcousticYMerger requires two inports.")

        #calculate outports
        (x1, y1, dx, dy) = self.inports[0]
        (x2, y2, dx2, dy2) = self.inports[1]
        if np.abs(dx * dy2 - dy * dx2) > 1E-10:
            print(colored("[optohedgehog WARNING] class AcousticYMerger: two inports not parallel, direction of the first port is used", color = "blue"))

        Lalign = 0.5 * np.abs((x2 - x1) * dx + (y2 - y1) * dy)
        if Lalign > 1E-6:
            print(colored(f"[optohedgehog WARNING] class AcousticYMerger: two inports not aligned, auto aligned, distance {2.0*Lalign} um", color="blue"))

        tmpl = 1.0/np.sqrt(dx*dx + dy*dy)
        dx *= tmpl
        dy *= tmpl
        nx = dy
        ny = -dx
        L = shift
        W = (x2-x1)*nx + (y2-y1)*ny   # no abs value, to distinguish port 1 and port 2

        x = 0.5 * (x1 + x2) + (L+Lalign) * dx
        y = 0.5 * (y1 + y2) + (L+Lalign) * dy
        self.outports = [(x, y, dx, dy)]

        #merger is reverse of the splitter, reverse (dx, dy)
        dx = -dx
        dy = -dy

        # generate real control points list 1
        self.refLength = 0.0
        cx1 = x + 0.3 * L * dx
        cy1 = y + 0.3 * L * dy
        cx2 = x + 0.6 * L * dx
        cy2 = y + 0.6 * L * dy
        cx3 = x + 0.6 * L * dx - 0.5 * W * nx
        cy3 = y + 0.6 * L * dy - 0.5 * W * ny
        cx4 = x + 1.0 * L * dx - 0.5 * W * nx
        cy4 = y + 1.0 * L * dy - 0.5 * W * ny
        self.controlpoints1 = [ (x,y), (cx1, cy1), (cx2, cy2),(cx3, cy3),(cx4, cy4) ]

        # generate real control points list 2
        self.refLength = 0.0
        cx1 = x + 0.3 * L * dx
        cy1 = y + 0.3 * L * dy
        cx2 = x + 0.6 * L * dx
        cy2 = y + 0.6 * L * dy
        cx3 = x + 0.6 * L * dx + 0.5 * W * nx
        cy3 = y + 0.6 * L * dy + 0.5 * W * ny
        cx4 = x + 1.0 * L * dx + 0.5 * W * nx
        cy4 = y + 1.0 * L * dy + 0.5 * W * ny
        self.controlpoints2 = [ (x,y), (cx1, cy1), (cx2, cy2),(cx3, cy3),(cx4, cy4) ]


        lastx = x
        lasty = y
        #calculate reference length for generating points
        for shiftx, shifty in self.controlpoints1:
            self.refLength += np.sqrt((shiftx-lastx)*(shiftx-lastx) + (shifty-lasty)*(shifty-lasty))
            lastx = shiftx
            lasty = shifty



        self.createmask()

    def createmask(self):
        (x1, y1, dx, dy) = self.inports[0]
        (x2, y2, dx2, dy2) = self.inports[1]

        #generate path 1
        nodes1 = np.asfortranarray(np.transpose(self.controlpoints1))
        curve = bezier.curve.Curve.from_nodes(nodes1)

        segN = int(float(self.refLength) / config.dfAcuRes + 5)
        segs = np.linspace(0.0, 1.0, segN)
        nodes1 = curve.evaluate_multi(segs)

        nodes1 = np.append(np.transpose(nodes1), [(x1,y1)], axis=0)   # fix the alignment of two ports

        self.path1 = nodes1
        wg1out, wg1in = _createAcousticNegWGmask(nodes1, width=config.dfAcuwgWidth, etchlayer=0, beforeBool=True)

        #generate path 2
        nodes2 = np.asfortranarray(np.transpose(self.controlpoints2))
        curve = bezier.curve.Curve.from_nodes(nodes2)

        segN = int(float(self.refLength) / config.dfAcuRes + 5)
        segs = np.linspace(0.0, 1.0, segN)
        nodes2 = curve.evaluate_multi(segs)

        nodes2 = np.append(np.transpose(nodes2), [(x2,y2)], axis=0)   # fix the alignment of two ports

        self.path2 = nodes2
        wg2out, wg2in = _createAcousticNegWGmask(nodes2, width=config.dfAcuwgWidth, etchlayer=0, beforeBool=True)

        #boolean and merge two path
        wgs = gdspy.boolean([wg1out,wg2out],[wg1in,wg2in], "not", precision=0.01, layer=self.layer, max_points=config.MAXPOINTS)
        self.add(wgs)

        return None
#end of class AcousticYMerger





def _createAcousticNegWGmask(path, width, etchlayer : int, *, straight=False, beforeBool = False):

    #if width is not an array extend to a numpy dnarray
    if hasattr(width, "__getitem__"):
        width0 = np.array(width)
    else:
        width0 = np.zeros(len(path)) + width


    currentOutLeftPoints = []
    currentOutRightPoints = []
    currentInLeftPoints = []
    currentInRightPoints = []

    (xlast, ylast) = path[0]
    FlagFirstpoint = True

    for (xcurrent, ycurrent), widthcurrent in zip(path[1:], width0[1:]):
        # print("path point:  ", xcurrent, ycurrent, widthcurrent)
        dx = xcurrent - xlast
        dy = ycurrent - ylast
        dxn = -dy
        dyn = dx
        if float(dxn * dxn + dyn * dyn)< 1e-8:   # skip repeated points
            continue
        revl = 1.0 / np.sqrt(float(dxn * dxn + dyn * dyn))
        dxn *= revl
        dyn *= revl

        if FlagFirstpoint:
            nodeOutLeft = (xlast + dxn * (width0[0] + config.dfAcuwgExtend) * 0.5,
                        ylast + dyn * (width0[0] + config.dfAcuwgExtend)* 0.5 )
            nodeOutRight = (xlast - dxn* (width0[0] + config.dfAcuwgExtend)* 0.5,
                         ylast - dyn * (width0[0] + config.dfAcuwgExtend)* 0.5 )
            nodeInLeft = (xlast + dxn * width0[0]* 0.5,
                          ylast + dyn * width0[0]* 0.5)
            nodeInRight = (xlast - dxn * width0[0]* 0.5,
                           ylast - dyn * width0[0]* 0.5)

            currentInLeftPoints.append(nodeInLeft)
            currentInRightPoints.append(nodeInRight)
            currentOutLeftPoints.append(nodeOutLeft)
            currentOutRightPoints.append(nodeOutRight)

            FlagFirstpoint = False

        nodeOutLeft = (xcurrent + dxn * (widthcurrent + config.dfAcuwgExtend) * 0.5,
                      ycurrent + dyn * (widthcurrent + config.dfAcuwgExtend) * 0.5)
        nodeOutRight = (xcurrent - dxn * (widthcurrent + config.dfAcuwgExtend) * 0.5,
                       ycurrent - dyn * (widthcurrent + config.dfAcuwgExtend) * 0.5)
        nodeInLeft = (xcurrent + dxn * widthcurrent * 0.5,
                       ycurrent + dyn * widthcurrent * 0.5)
        nodeInRight = (xcurrent - dxn * widthcurrent * 0.5,
                        ycurrent - dyn * widthcurrent * 0.5)

        currentInLeftPoints.append(nodeInLeft)
        currentInRightPoints.append(nodeInRight)
        currentOutLeftPoints.append(nodeOutLeft)
        currentOutRightPoints.append(nodeOutRight)

        xlast = xcurrent
        ylast = ycurrent
    # end for loop

    #fix the precision issue of boolean operation -- extent the inner path at both ends
    #end point
    xlast, ylast = currentInLeftPoints[-1]
    seclastx, seclasty = currentInLeftPoints[-2]
    extx = 2.0 * xlast - seclastx
    exty = 2.0 * ylast - seclasty
    currentInLeftPoints.append((extx, exty))

    xlast, ylast = currentInRightPoints[-1]
    seclastx, seclasty = currentInRightPoints[-2]
    extx = 2.0 * xlast - seclastx
    exty = 2.0 * ylast - seclasty
    currentInRightPoints.append((extx, exty))

    currentInRightPoints.reverse()
    currentOutRightPoints.reverse()

    #start point
    xlast, ylast = currentInRightPoints[-1]
    seclastx, seclasty = currentInRightPoints[-2]
    extx = 2.0 * xlast - seclastx
    exty = 2.0 * ylast - seclasty
    currentInRightPoints.append((extx, exty))

    xlast, ylast = currentInLeftPoints[0]
    seclastx, seclasty = currentInLeftPoints[1]
    extx = 2.0 * xlast - seclastx
    exty = 2.0 * ylast - seclasty
    currentInRightPoints.append((extx, exty))    #this should add to the Right, and end of Right boundary is equivlent to the beigning of left

    outPath = gdspy.Polygon([*currentOutLeftPoints, *currentOutRightPoints])
    # outPath = outPath.fracture()
    inPath = gdspy.Polygon([*currentInLeftPoints, *currentInRightPoints], layer = 1)
    # inPath = inPath.fracture()

    if beforeBool:
        return outPath, inPath
    else:
        maskPath = gdspy.boolean(outPath, inPath, "not", layer=etchlayer, precision =0.001, max_points=config.MAXPOINTS)
        return maskPath


#end of _createAcousticWGmask





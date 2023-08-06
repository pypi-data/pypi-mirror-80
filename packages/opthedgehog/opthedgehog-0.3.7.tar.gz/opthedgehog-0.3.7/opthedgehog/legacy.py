#############################
#  This files contains retired functions / patterns
#
############################

from gdspy import Cell
import gdspy
import numpy as np
import bezier
import warnings
from typing import Tuple, List
from termcolor import colored

from .optCells import OptCell


from . import config

class OptParallelArcTanConnect(OptCell):
    curvepos = 0.5

    def __init__(self, name, inport, outport, curvepos, layer=10):
        OptCell.__init__(self, name, layer)
        self.inports = list([inport])
        self.outports = list([outport])
        self.curvepos = curvepos
        self.createmask()

    def createmask(self):
        path = []
        x1 = self.inports[0][0]
        y1 = self.inports[0][1]
        x2 = self.outports[0][0]
        y2 = self.outports[0][1]

        if x2 < x1:
            tmp = x1
            x1 = x2
            x2 = tmp
            tmp = y1
            y1 = y2
            y2 = tmp

        if y1 == y2:
            path.append((x1, y1))
            path.append((x2, y2))
        else:
            a = y2 - y1
            b = min(abs(a), 20.0)
            yc = float(y1 + y2) / 2.0
            xc = self.curvepos * x2 + (1.0 - self.curvepos) * x1

            if abs(xc - x1) < 5.0 * abs(b) or abs(xc - x2) < 5.0 * abs(b):
                print("[ERROR] OptParrllelConnect -- curve pos too close to the port")
                return

            path.append((x1, y1))
            path.append((xc - 5.0 * b, y1))

            for xt in np.arange(-5.0 * abs(b), 5.0 * abs(b), 0.05, dtype=float):
                yt = 1.04218 * float(a) / np.pi * np.arctan(np.pi / float(b) * (xt)) + yc
                path.append((xt + xc, yt))

            path.append((xc + 5.0 * b, y2))
            path.append((x2, y2))

        wg2 = gdspy.PolyPath(path, width=config.dfoptwgwidth, max_points=199, layer=self.layer, corners=1)
        self.add(wg2)


class OptParallelBezierConnect(OptCell):
    """
       using Bezier for curved optical waveguide
    """
    pathnodes = []  # strage the nodes of the Bezier curve

    def __init__(self, name, inport, shift, layer=10):
        OptCell.__init__(self, name=name, layer=layer)
        if isinstance(inport, list):
            self.inports = inport
        else:
            self.inports = [inport]

        (x, y, dx, dy) = self.inports[0]
        self.outports = [(x + shift[0], y + shift[1], dx, dy)]
        self.pathnodes = []
        self.createmask()

    def createmask(self):
        (x0, y0, tmp, tmp) = self.inports[0]
        (xend, yend, tmp, tmp) = self.outports[0]
        x1 = x2 = (float(x0 + xend)) / 2.0
        y1 = y0
        y2 = yend
        nodes = np.asfortranarray([
            [x0, x1, x2, xend],
            [y0, y1, y2, yend],
        ])
        curve = bezier.curve.Curve.from_nodes(nodes)

        dist = max(abs(yend - y0), abs(xend - x0))
        segN = int(float(dist) / 0.05 + 5)
        segs = np.linspace(0.0, 1.0, segN)
        nodes = curve.evaluate_multi(segs)

        nodes = np.transpose(nodes)
        self.pathnodes = nodes
        wg = gdspy.PolyPath(nodes, width=config.dfoptwgwidth, max_points=199, layer=self.layer, corners=1)
        self.add(wg)
        return None
    #end of OptParallelBezierConnect


class OptRaceTrackCavityVC(OptCell):
    """

    """

    xleftcenter = 0.0
    yleftcenter = 0.0
    xrightcenter = 0.0
    yrightcenter = 0.0
    cavityradius = 0.0
    couplinggap = 0.0
    cavityRacinglength = 0.0
    pathnodes = []
    pathcavity = []
    direction = -1

    def __init__(self, name, inport, cavityradius, cavityRacinglength, couplinggap, layer=10, direction=-1):
        OptCell.__init__(self, name, layer)
        if isinstance(inport, list):
            self.inports = inport[0:1]
        else:
            self.inports = [inport]
        self.direction = direction

        (x, y, dx, dy) = self.inports[0]
        self.outports = [(x + 2*cavityradius , y + 3*cavityradius , 1.0, 0)]
        self.cavityradius = cavityradius
        self.couplinggap = couplinggap
        self.cavityRacinglength = cavityRacinglength
        self.pathnodes = []
        self.pathcavity = []
        self.xleftcenter = self.yleftcenter = self.xrightcenter = self.yrightcenter = 0.0
        self.createmaskCouplingWG()
        self.createmaskCavity()

    def createmaskCouplingWG(self):
        (x0, y0, dx, dy) = self.inports[0]
        # first curve
        nodeslist1 = np.asfortranarray([
            [x0, x0+self.cavityradius, x0+self.cavityradius],
            [y0, y0,                   y0+self.cavityradius],
        ])
        curve = bezier.curve.Curve.from_nodes(nodeslist1)

        dist = self.cavityradius
        segN = int(float(dist) / 0.05 + 3)
        segs = np.linspace(0.0, 1.0, segN)
        nodes = curve.evaluate_multi(segs)

        nodes = np.transpose(nodes)
        self.pathnodes.extend(nodes)
        wgSeg1 = gdspy.PolyPath(nodes, width=config.dfoptwgwidth, max_points=199, layer=self.layer, corners=1)
        self.add(wgSeg1)

        #verticle segment
        nodesVerticleList = [(x0+self.cavityradius, y0+self.cavityradius),(x0+self.cavityradius, y0+2.0*self.cavityradius)]
        ## add addition points to simplify suspended opening genration
        segN = int(self.cavityradius / 0.1 + 3)
        for i in np.linspace(0.0, 1.0 ,segN):
            xt = i*nodesVerticleList[1][0] + (1.0-i)*nodesVerticleList[0][0]
            yt = i*nodesVerticleList[1][1] + (1.0-i)*nodesVerticleList[0][1]
            self.pathnodes.append((xt,yt))

        wgSeg2 = gdspy.PolyPath(nodesVerticleList, width=config.dfoptwgwidth, max_points=199, layer=self.layer, corners=1)
        self.add(wgSeg2)

        #second curve
        nodeslist2 = np.asfortranarray([
            [x0 + self.cavityradius, x0 + self.cavityradius, x0 + 2.0*self.cavityradius ],
            [y0+2.0*self.cavityradius, y0+3.0*self.cavityradius, y0+3.0*self.cavityradius]
        ])
        curve2 = bezier.curve.Curve.from_nodes(nodeslist2)

        dist = self.cavityradius
        segN = int(float(dist) / 0.05 + 3)
        segs2 = np.linspace(0.0, 1.0, segN)
        nodes2 = curve2.evaluate_multi(segs2)

        nodes2 = np.transpose(nodes2)
        self.pathnodes.extend(nodes2)
        wgSeg3 = gdspy.PolyPath(nodes2, width=config.dfoptwgwidth, max_points=199, layer=self.layer, corners=1)
        self.add(wgSeg3)

        return 0

    def createmaskCavity(self):
        (x0, y0, dx, dy) = self.inports[0]

        # left round part
        self.xleftcenter = x0 + self.cavityradius + (self.couplinggap + config.dfoptwgwidth + self.cavityradius)
        self.yleftcenter = y0 + self.cavityradius * 1.5

          # add to cavity path
        for i in np.linspace(0.5*np.pi, 1.5*np.pi, int(self.cavityradius*np.pi/0.05)):
            self.pathcavity.append(
                (self.xleftcenter + self.cavityradius*np.cos(i), self.yleftcenter + self.cavityradius* np.sin(i))
            )

        cavityleft = gdspy.Round((self.xleftcenter, self.yleftcenter),
                              radius=self.cavityradius + config.dfoptwgwidth / 2,
                              inner_radius=self.cavityradius - config.dfoptwgwidth / 2,
                              initial_angle= 0.5*np.pi,
                              final_angle= 1.5*np.pi,
                              number_of_points= int(self.cavityradius*np.pi/0.05+3) ,
                              layer=self.layer)
        self.add(cavityleft)


        #bottom straight waveguide
        nodes = [(self.xleftcenter , self.yleftcenter - self.cavityradius),
                 (self.xleftcenter + self.cavityRacinglength, self.yleftcenter - self.cavityradius)]
        ## add addition points to simplify suspended opening genration
        segN = int(self.cavityRacinglength / 0.1 + 3)
        for i in np.linspace(0.0, 1.0, segN):
            xt = i * nodes[1][0] + (1.0 - i) * nodes[0][0]
            yt = i * nodes[1][1] + (1.0 - i) * nodes[0][1]
            self.pathcavity.append((xt, yt))
        wgSeg = gdspy.PolyPath(nodes, width=config.dfoptwgwidth, max_points=199, layer=self.layer, corners=1)
        self.add(wgSeg)

        # right round part
        self.xrightcenter = self.xleftcenter + self.cavityRacinglength
        self.yrightcenter = self.yleftcenter

        # add to cavity path
        for i in np.linspace(-0.5 * np.pi, 0.5 * np.pi, int(self.cavityradius * np.pi / 0.05)):
            self.pathcavity.append(
                (self.xrightcenter + self.cavityradius * np.cos(i), self.yrightcenter + self.cavityradius * np.sin(i))
            )

        cavityleft = gdspy.Round((self.xrightcenter, self.yrightcenter),
                                 radius=self.cavityradius + config.dfoptwgwidth / 2,
                                 inner_radius=self.cavityradius - config.dfoptwgwidth / 2,
                                 initial_angle=-0.5 * np.pi,
                                 final_angle=0.5 * np.pi,
                                 number_of_points=int(self.cavityradius * np.pi / 0.05),
                                 layer=self.layer)
        self.add(cavityleft)


        #top straight waveguide
        nodes = [(self.xrightcenter , self.yrightcenter + self.cavityradius),
                 (self.xleftcenter, self.yleftcenter + self.cavityradius)]
        ## add addition points to simplify suspended opening genration
        segN = int(self.cavityRacinglength / 0.1 + 3)
        for i in np.linspace(0.0, 1.0, segN):
            xt = i * nodes[1][0] + (1.0 - i) * nodes[0][0]
            yt = i * nodes[1][1] + (1.0 - i) * nodes[0][1]
            self.pathcavity.append((xt, yt))
        wgSeg = gdspy.PolyPath(nodes, width=config.dfoptwgwidth, max_points=199, layer=self.layer, corners=1)
        self.add(wgSeg)

        return 0
    #end of ptRaceTrackCa


class OptCoupledRaceTrack(OptCell):
    """
    coupled waveguides with both coupling waveguide
    """
    cavityradius = 0.0
    cavityRacinglength = 0.0
    WGcplGap = 0.0
    CavitycplGap = 0.0
    ringwidth = 0.0
    cavity1L = (0.0, 0.0)
    cavity1R = (0.0, 0.0)
    cavity2L = (0.0, 0.0)
    cavity2R = (0.0, 0.0)
    localconfig = config

    path_wg1 = []
    path_wg2 = []
    path_cavity1 = []
    path_cavity2 = []

    def __init__(self, name, inport, cavityradius, cavityRacinglength, WGcplGap, cavitycplGap, ringwidth=config.dfoptwgwidth, layer=10):
        OptCell.__init__(self, name, layer)
        if isinstance(inport, list):
            if len(inport)>=2:
                self.inports = inport[0:2]
            else:
                self.inports = inport[0]
                warnings.warn("[OptHedgehog Warning] Class OptCoupledRaceTrack only one inport found, dead end optical waveguide generated.")
                (x, y, dx, dy) = inport[0]
                self.inports.append( (x, y - 100.0, dx, dy) )
        else:
            (x, y, dx, dy) = inport
            self.inports = [inport]
            warnings.warn("[OptHedgehog Warning] Class OptCoupledRaceTrack only one inport found, dead end optical waveguide generated."
                          "  port "+str(inport))
            self.inports.append( ((x, y - 100.0, dx, dy)))

        self.cavityradius = cavityradius
        self.cavityRacinglength = cavityRacinglength
        self.WGcplGap = WGcplGap
        self.CavitycplGap = cavitycplGap
        self.ringwidth = ringwidth

        self.createmaskCavities()
        self.createmaskCouplingWG1()
        self.createmaskCouplingWG2()
        self.createGuideFields()
        pass

    def createmaskCavities(self):
        ### determine reference points ####
        (x1, y1, tmp, tmp) = self.inports[0]
        self.cavity1L = (  x1 + config.dfTurningRadius + self.WGcplGap + config.dfoptwgwidth*0.5 + self.ringwidth*0.5 + self.cavityradius
                           , y1 + config.dfTurningRadius + 0.5*self.cavityradius)
        (c1Lx, c1Ly) = self.cavity1L
        self.cavity1R = (c1Lx + self.cavityRacinglength, c1Ly)

        c2Lx = c1Lx
        c2Ly  = c1Ly + 2.0*self.cavityradius + self.CavitycplGap
        c2Rx = c2Lx + self.cavityRacinglength
        c2Ry = c2Ly
        self.cavity2L = (c2Lx, c2Ly)
        self.cavity2R = (c2Rx, c2Ry)


        # add cavity waveguides
        #cavity one
        self.path_cavity1 = []
        (x1, y1) = self.cavity1L
        y1 = y1 - self.cavityradius
        x2 = x1 + self.cavityRacinglength
        y2 = y1
        dist = x2 - x1
        N = dist / 0.08 + 2
        nodes = [(x1+ i*dist, y1) for i in np.arange(0.0, 1.0, 1.0 / N)]
        self.path_cavity1.extend(nodes)

        #turn up
        x3 = self.cavity1R[0] + self.cavityradius
        y3 = y2
        x4 = x3
        y4 = y3 + self.cavityradius

        nodes = _ThreePointTurning([x2, x3, x4],
                                   [y2, y3, y4])
        self.path_cavity1.extend(nodes)

        #turn
        x5 = x4
        y5 = y4 + self.cavityradius
        x6 = x5 - self.cavityradius
        y6 = y5
        nodes = _ThreePointTurning([x4, x5, x6],
                                   [y4, y5, y6])
        self.path_cavity1.extend(nodes)

        #top
        x7 = x6 - self.cavityRacinglength
        y7 = y6
        dist = - self.cavityRacinglength
        N = dist / 0.08 + 2
        nodes = [ (x6 + i * dist, y6) for i in np.arange(0.0, 1.0, 1.0 / N ) ]
        self.path_cavity1.extend(nodes)

        #left
        x8 = self.cavity1L[0] - self.cavityradius
        y8 = y7
        x9 = x8
        y9 = self.cavity1L[1]
        nodes = _ThreePointTurning([x7, x8, x9],
                                   [y7, y8, y9])
        self.path_cavity1.extend(nodes)

        #left down
        x10 = x9
        y10 = y9 - self.cavityradius
        x11 = x10 + self.cavityradius
        y11 = y10
        nodes = _ThreePointTurning([x9, x10, x11],
                                   [y9, y10, y11])
        self.path_cavity1.extend(nodes)

        # add mask
        cavity1 = gdspy.PolyPath(self.path_cavity1, width=self.ringwidth, max_points=199, layer=self.layer)
        self.add(cavity1)


        #Cavity TWO
        self.path_cavity2 = []
        (x1, y1) = self.cavity2L
        y1 = y1 - self.cavityradius
        x2 = x1 + self.cavityRacinglength
        y2 = y1
        dist = x2 - x1
        N = dist / 0.08 + 2
        nodes = [(x1+ i*dist, y1) for i in np.arange(0.0, 1.0, 1.0 / N)]
        self.path_cavity2.extend(nodes)

        #turn up
        x3 = self.cavity2R[0] + self.cavityradius
        y3 = y2
        x4 = x3
        y4 = y3 + self.cavityradius

        nodes = _ThreePointTurning([x2, x3, x4],
                                   [y2, y3, y4])
        self.path_cavity2.extend(nodes)

        #turn
        x5 = x4
        y5 = y4 + self.cavityradius
        x6 = x5 - self.cavityradius
        y6 = y5
        nodes = _ThreePointTurning([x4, x5, x6],
                                   [y4, y5, y6])
        self.path_cavity2.extend(nodes)

        #top
        x7 = x6 - self.cavityRacinglength
        y7 = y6
        dist = - self.cavityRacinglength
        N = dist / 0.08 + 2
        nodes = [ (x6 + i * dist, y6) for i in np.arange(0.0, 1.0, 1.0 / N ) ]
        self.path_cavity2.extend(nodes)

        #left
        x8 = self.cavity2L[0] - self.cavityradius
        y8 = y7
        x9 = x8
        y9 = self.cavity2L[1]
        nodes = _ThreePointTurning([x7, x8, x9],
                                   [y7, y8, y9])
        self.path_cavity2.extend(nodes)

        #left down
        x10 = x9
        y10 = y9 - self.cavityradius
        x11 = x10 + self.cavityradius
        y11 = y10
        nodes = _ThreePointTurning([x9, x10, x11],
                                   [y9, y10, y11])
        self.path_cavity2.extend(nodes)

        # add mask
        cavity2 = gdspy.PolyPath(self.path_cavity2, width=self.ringwidth, max_points=199, layer=self.layer)
        self.add(cavity2)



        pass

    def createmaskCouplingWG1(self):
        """ Left coupling waveguide. """
        self.path_wg1 = []
        (x1, y1, tmp, tmp) = self.inports[0]
        x2 = self.cavity1L[0] - self.cavityradius - self.WGcplGap - config.dfoptwgwidth*0.5 - self.ringwidth*0.5
        y2 = y1
        x3 = x2
        y3 = y1 + config.dfTurningRadius
        nodes = _ThreePointTurning([x1, x2, x3],
                                   [y1, y2, y3] )
        self.path_wg1.extend(nodes)

        # straight up
        N = config.dfTurningRadius / 0.08 + 2
        nodes = [ (x3, y3 + i*config.dfTurningRadius) for i in np.arange(0.0, 1.0, 1.0 / N)]
        self.path_wg1.extend(nodes)
        x4 = x3
        y4 = y3 + config.dfTurningRadius

        # Turning to left
        x5 = x4
        y5 = y4 + config.dfTurningRadius
        x6 = x5 - config.dfTurningRadius
        y6 = y5
        nodes = _ThreePointTurning(
            [x4, x5, x6],
            [y4, y5, y6],
        )
        self.path_wg1.extend(nodes)

        # Turning up
        x7 = x6 - 2 * config.dfTurningRadius
        y7 = y6
        x8 = x7
        y8 = y7 + config.dfTurningRadius
        nodes = _ThreePointTurning([x6, x7, x8],
                                   [y6, y7, y8])
        self.path_wg1.extend(nodes)

        #straight up
        dist = 5*self.cavityradius - 4*config.dfTurningRadius
        N = dist / 0.08 + 2
        nodes = [(x8, y8 + i * dist) for i in np.arange(0.0, 1.0, 1.0 / N)]
        x9 = x8
        y9 = y8 + dist
        self.path_wg1.extend(nodes)

        #Turning left
        x10 = x9
        y10 = y9 + config.dfTurningRadius
        x11 = x10 + config.dfTurningRadius
        y11 = y10
        nodes = _ThreePointTurning([x9, x10, x11],
                                   [y9, y10, y11])
        self.path_wg1.extend(nodes)

        #Straight to right
        dist = 4.0 * config.dfTurningRadius + 2.0 * self.cavityradius + self.cavityRacinglength
        x12 = x11 + dist
        y12 = y11
        N = dist / 0.08 + 2
        nodes = [(x11 + i*dist, y12) for i in np.arange(0.0, 1.0, 1.0 / N)]
        self.path_wg1.extend(nodes)

        #add waveguide mask.
        self.outports.append((x12, y12, 1, 0))
        wg1 = gdspy.PolyPath(self.path_wg1, width=config.dfoptwgwidth, max_points=199, layer=self.layer)
        self.add(wg1)

        pass

    def createmaskCouplingWG2(self):
        """ Left coupling waveguide. """
        self.path_wg2 = []
        (x1, y1, tmp, tmp) = self.inports[1]



        # straight RIGHT
        x2 = self.inports[0][0] + 2.0*config.dfTurningRadius + 2*self.cavityradius + self.cavityRacinglength
        y2 = y1
        dist = x2 - x1
        N = dist / 0.08 + 2
        nodes = [ (x1 + i*dist, y1 ) for i in np.arange(0.0, 1.0, 1.0 / N)]
        self.path_wg2.extend(nodes)

        #turning UP
        x3 = x2 + config.dfTurningRadius
        y3 = y2
        x4 = x3
        y4 = y2 + config.dfTurningRadius
        nodes = _ThreePointTurning([x2, x3, x4],
                                   [y2, y3, y4] )
        self.path_wg2.extend(nodes)

        # straight UP
        x5 = x4
        y5 = self.cavity2R[1] - 0.5 * self.cavityradius - 2.0*config.dfTurningRadius
        dist = y5 - y4
        N = dist / 0.08 + 2
        nodes = [ (x4, y4 + i*dist) for i in np.arange(0.0, 1.0, 1.0 / N)]
        self.path_wg2.extend(nodes)

        # Turning to left
        x6 = x5
        y6 = y5 + config.dfTurningRadius
        x7 = x6 - config.dfTurningRadius
        y7 = y6
        nodes = _ThreePointTurning(
            [x5, x6, x7],
            [y5, y6, y7],
        )
        self.path_wg2.extend(nodes)

        # Turning up
        x8 = self.cavity2R[0] + self.cavityradius + config.dfoptwgwidth + self.WGcplGap
        y8 = y7
        x9 = x8
        y9 = y8 + config.dfTurningRadius
        nodes = _ThreePointTurning([x7, x8, x9],
                                   [y7, y8, y9])
        self.path_wg2.extend(nodes)

        #straight up
        dist = self.cavityradius
        N = dist / 0.08 + 2
        nodes = [(x9, y9 + i * dist) for i in np.arange(0.0, 1.0, 1.0 / N)]
        x10 = x9
        y10 = y9 + dist
        self.path_wg2.extend(nodes)

        #Turning left
        x11 = x10
        y11 = self.outports[0][1] + self.inports[1][1] - self.inports[0][1]
        x12 = x11 + config.dfTurningRadius
        y12 = y11
        nodes = _ThreePointTurning([x10, x11, x12],
                                   [y10, y11, y12])
        self.path_wg2.extend(nodes)

        #Straight to right
        x13 = self.outports[0][0]
        y13 = y12
        dist = x13 - x12
        N = dist / 0.08 + 2
        nodes = [(x12 + i*dist, y13) for i in np.arange(0.0, 1.0, 1.0 / N)]
        self.path_wg2.extend(nodes)

        #add waveguide mask.
        self.outports.append((x13, y13, 1, 0))
        wg2 = gdspy.PolyPath(self.path_wg2, width=config.dfoptwgwidth, max_points=199, layer=self.layer)
        self.add(wg2)

        pass

    def createGuideFields(self):
        xcenter = (self.cavity2L[0]+self.cavity2R[0]) / 2.0
        ycenter = (self.cavity1L[1]+self.cavity2L[1]) / 2.0
        fieldrec = gdspy.Rectangle((xcenter - config.dfFieldSize/2.0, ycenter - config.dfFieldSize/2.0),
                                   (xcenter + config.dfFieldSize/2.0, ycenter + config.dfFieldSize/2.0),
                                   layer = config.dfFieldGuideLayer)
        self.add(fieldrec)
        pass
    # end of OptCoupledRaceTrack


class OptSingleEMAORaceTrack(OptCell):
    """
    Reuse the code from OptCoupledTaceTrack, but disable one cavity.  keep optical cavity 2
    """
    cavityradius = 0.0
    cavityRacinglength = 0.0
    WGcplGap = 0.0
    CavitycplGap = 0.0
    ringwidth = 0.0
    cavity1L = (0.0, 0.0)
    cavity1R = (0.0, 0.0)
    cavity2L = (0.0, 0.0)
    cavity2R = (0.0, 0.0)
    localconfig = config

    path_wg1 = []
    path_wg2 = []
    path_cavity1 = []
    path_cavity2 = []

    def __init__(self, name, inport, cavityradius, cavityRacinglength, WGcplGap, ringwidth=config.dfoptwgwidth, layer=10):
        OptCell.__init__(self, name, layer)
        if isinstance(inport, list):
           self.inports = inport
        else:
           self.inports = [inport]

        self.cavityradius = cavityradius
        self.cavityRacinglength = cavityRacinglength
        self.WGcplGap = WGcplGap
        self.CavitycplGap = 0.0
        self.ringwidth = ringwidth

        self.createmaskCavities()
        #self.createmaskCouplingWG1()
        self.createmaskCouplingWG2()
        self.createGuideFields()
        pass

    def createmaskCavities(self):
        ### determine reference points ####
        (x1, y1, tmp, tmp) = self.inports[0]
        self.cavity1L = (  x1 + config.dfTurningRadius + self.WGcplGap + config.dfoptwgwidth*0.5 + self.ringwidth*0.5 + self.cavityradius
                           , y1 + config.dfTurningRadius + 0.5*self.cavityradius)
        (c1Lx, c1Ly) = self.cavity1L
        self.cavity1R = (c1Lx + self.cavityRacinglength, c1Ly)

        c2Lx = c1Lx
        c2Ly  = c1Ly + 2.0*self.cavityradius + self.CavitycplGap
        c2Rx = c2Lx + self.cavityRacinglength
        c2Ry = c2Ly
        self.cavity2L = (c2Lx, c2Ly)
        self.cavity2R = (c2Rx, c2Ry)


        #Cavity TWO
        self.path_cavity2 = []
        (x1, y1) = self.cavity2L
        y1 = y1 - self.cavityradius
        x2 = x1 + self.cavityRacinglength
        y2 = y1
        dist = x2 - x1
        N = dist / 0.08 + 2
        nodes = [(x1+ i*dist, y1) for i in np.arange(0.0, 1.0, 1.0 / N)]
        self.path_cavity2.extend(nodes)

        #turn up
        x3 = self.cavity2R[0] + self.cavityradius
        y3 = y2
        x4 = x3
        y4 = y3 + self.cavityradius

        nodes = _ThreePointTurning([x2, x3, x4],
                                   [y2, y3, y4])
        self.path_cavity2.extend(nodes)

        #turn
        x5 = x4
        y5 = y4 + self.cavityradius
        x6 = x5 - self.cavityradius
        y6 = y5
        nodes = _ThreePointTurning([x4, x5, x6],
                                   [y4, y5, y6])
        self.path_cavity2.extend(nodes)

        #top
        x7 = x6 - self.cavityRacinglength
        y7 = y6
        dist = - self.cavityRacinglength
        N = dist / 0.08 + 2
        nodes = [ (x6 + i * dist, y6) for i in np.arange(0.0, 1.0, 1.0 / N ) ]
        self.path_cavity2.extend(nodes)

        #left
        x8 = self.cavity2L[0] - self.cavityradius
        y8 = y7
        x9 = x8
        y9 = self.cavity2L[1]
        nodes = _ThreePointTurning([x7, x8, x9],
                                   [y7, y8, y9])
        self.path_cavity2.extend(nodes)

        #left down
        x10 = x9
        y10 = y9 - self.cavityradius
        x11 = x10 + self.cavityradius
        y11 = y10
        nodes = _ThreePointTurning([x9, x10, x11],
                                   [y9, y10, y11])
        self.path_cavity2.extend(nodes)

        # add mask
        cavity2 = gdspy.PolyPath(self.path_cavity2, width=self.ringwidth, max_points=199, layer=self.layer)
        self.add(cavity2)



        pass

    def createmaskCouplingWG1(self):
        """
        Deleted for single cavity configuration
        :return:
        """
        pass

    def createmaskCouplingWG2(self):
        """ Left coupling waveguide. """
        self.path_wg2 = []
        (x1, y1, tmp, tmp) = self.inports[0]   #Changed to the first port for single cavity


        # straight RIGHT
        x2 = self.inports[0][0] + 2.0*config.dfTurningRadius + 2*self.cavityradius + self.cavityRacinglength
        y2 = y1
        dist = x2 - x1
        N = dist / 0.08 + 2
        nodes = [ (x1 + i*dist, y1 ) for i in np.arange(0.0, 1.0, 1.0 / N)]
        self.path_wg2.extend(nodes)

        #turning UP
        x3 = x2 + config.dfTurningRadius
        y3 = y2
        x4 = x3
        y4 = y2 + config.dfTurningRadius
        nodes = _ThreePointTurning([x2, x3, x4],
                                   [y2, y3, y4] )
        self.path_wg2.extend(nodes)

        # straight UP
        x5 = x4
        y5 = self.cavity2R[1] - 0.5 * self.cavityradius - 2.0*config.dfTurningRadius
        dist = y5 - y4
        N = dist / 0.08 + 2
        nodes = [ (x4, y4 + i*dist) for i in np.arange(0.0, 1.0, 1.0 / N)]
        self.path_wg2.extend(nodes)

        # Turning to left
        x6 = x5
        y6 = y5 + config.dfTurningRadius
        x7 = x6 - config.dfTurningRadius
        y7 = y6
        nodes = _ThreePointTurning(
            [x5, x6, x7],
            [y5, y6, y7],
        )
        self.path_wg2.extend(nodes)

        # Turning up
        x8 = self.cavity2R[0] + self.cavityradius + config.dfoptwgwidth + self.WGcplGap
        y8 = y7
        x9 = x8
        y9 = y8 + config.dfTurningRadius
        nodes = _ThreePointTurning([x7, x8, x9],
                                   [y7, y8, y9])
        self.path_wg2.extend(nodes)

        #straight up
        dist = self.cavityradius
        N = dist / 0.08 + 2
        nodes = [(x9, y9 + i * dist) for i in np.arange(0.0, 1.0, 1.0 / N)]
        x10 = x9
        y10 = y9 + dist
        self.path_wg2.extend(nodes)

        #Turning left
        x11 = x10
        y11 = y10 + config.dfTurningRadius
        x12 = x11 + config.dfTurningRadius
        y12 = y11
        nodes = _ThreePointTurning([x10, x11, x12],
                                   [y10, y11, y12])
        self.path_wg2.extend(nodes)

        #Straight to right
        x13 = x12 + config.dfTurningRadius
        y13 = y12
        dist = x13 - x12
        N = dist / 0.08 + 2
        nodes = [(x12 + i*dist, y13) for i in np.arange(0.0, 1.0, 1.0 / N)]
        self.path_wg2.extend(nodes)

        #add waveguide mask.
        self.outports.append((x13, y13, 1, 0))
        wg2 = gdspy.PolyPath(self.path_wg2, width=config.dfoptwgwidth, max_points=199, layer=self.layer)
        self.add(wg2)

        pass

    def createGuideFields(self):
        xcenter = (self.cavity2L[0]+self.cavity2R[0]) / 2.0
        ycenter = (self.cavity2L[1]+self.cavity2L[1]) / 2.0    # changed to cavity#2 for single cavity.
        fieldrec = gdspy.Rectangle((xcenter - config.dfFieldSize/2.0, ycenter - config.dfFieldSize/2.0),
                                   (xcenter + config.dfFieldSize/2.0, ycenter + config.dfFieldSize/2.0),
                                   layer = config.dfFieldGuideLayer)
        self.add(fieldrec)
        pass
    #end of OptSingleEMAORaceTrack


def _ThreePointTurning(xlist, ylist):
    x1 = xlist[0]
    x3 = xlist[-1]
    y1 = ylist[0]
    y3 = ylist[-1]

    nodes = np.asfortranarray([
        xlist,
        ylist,
    ])
    curve = bezier.curve.Curve.from_nodes(nodes, )

    dist = 1.454 * np.sqrt((x3-x1)*(x3-x1) + (y3-y1)*(y3-y1))
    segN = int(float(dist) / 0.08 + 5)
    segs = np.linspace(0.0, 1.0, segN)
    nodes = curve.evaluate_multi(segs)

    nodes = np.transpose(nodes)
    return nodes




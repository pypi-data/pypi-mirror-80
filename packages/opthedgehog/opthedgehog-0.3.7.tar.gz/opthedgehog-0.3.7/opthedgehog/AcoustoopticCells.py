######################################################################################
##  OptHedgehog ---
##   A Python package for integreated optices.
##  Description:
##     This files contains classes to generate acousto optic cells.
######################################################################################

#external modules
from gdspy import Cell
import gdspy
import numpy as np
import warnings

#internal files
# from config import dfIDTpitch, dfIDTwidth, dfIDTpadSize, dfIDTpadPitch, _index, dfOpeningOffset,\
#    dfOpeningWidth, dfOpeningConnection, dfAlignmentOverLay, dfIDTLongWiring
# The above import won't be sync'ed globally, and only take the value initionalized and not follew the change.
from . import config

from .IDTcells import _metalIDTFingers
from .optCells import OptStraightWaveguide
from .legacy import OptRaceTrackCavityVC, OptCoupledRaceTrack, OptSingleEMAORaceTrack
from .suspendedOptCell import _createsuspath







class AcoustoOptStraight4SegWaveguide(OptStraightWaveguide):
    """

    """
    suslayer = 20
    metallayer = 30
    slabSingleLength = 0.0
    slabWidth = 0.0
    slabN = 4
    IDToffset = 0.0
    IDTn = 0
    SAWresconatorConnection = 1.5
    def __init__(self, name, inports, slabSingleLength, slabWidth, IDToffset, IDTn, layer=10, suslayer = 20, metallayer = 30):
        self.slabN = 4
        self.SAWresconatorConnection = 1.5

        OptStraightWaveguide.__init__(self, name, inports, slabSingleLength*self.slabN + self.SAWresconatorConnection, layer)

        self.suslayer = suslayer
        self.metallayer = metallayer
        self.slabSingleLength = slabSingleLength
        self.slabWidth = slabWidth
        self.IDToffset = IDToffset
        self.IDTn = IDTn
        self.createIDT()
        self.createSuspendingOpening()

    def createSuspendingOpening(self):
        # top opening
        (x0, y0, tmp, tmp) = self.inports[0]
        for i in range(0,self.slabN):
            topopenOne = gdspy.Rectangle( (x0+self.SAWresconatorConnection, y0+config.dfOpeningOffset ),
                                   (x0 + self.slabSingleLength, y0 + config.dfOpeningOffset+1.5*config.dfOpeningWidth),
                                   layer=self.suslayer)
            x0 += self.slabSingleLength
            self.add([topopenOne])

        # bottom opening
        (x0, y0, tmp, tmp) = self.inports[0]
        for i in range(0,self.slabN):
            bottomopenOne = gdspy.Rectangle((x0 + self.SAWresconatorConnection, y0+config.dfOpeningOffset - self.slabWidth),
                                     (x0+self.slabSingleLength, y0 + config.dfOpeningOffset - self.slabWidth-1.5*config.dfOpeningWidth) ,
                                     layer=self.suslayer)
            x0 += self.slabSingleLength
            self.add([bottomopenOne])

        #left opening
        (x0, y0, tmp, tmp) = self.inports[0]
        leftopen = gdspy.Rectangle((x0-config.dfOpeningConnection, y0 - config.dfOpeningOffset ),
                                     (x0, y0 + config.dfOpeningOffset - self.slabWidth -  1.0*config.dfOpeningOffset) ,
                                     layer=self.suslayer)

        #right opening
        (x1, y1, tmp, tmp) = self.outports[0]
        rightopen = gdspy.Rectangle((x1 , y1 - config.dfOpeningOffset ),
                                     (x1 + config.dfOpeningConnection, y1 + config.dfOpeningOffset - self.slabWidth - 1.0*config.dfOpeningOffset) ,
                                     layer=self.suslayer)

        self.add([leftopen, rightopen])
        pass

    def createIDT(self):
        (x0, y0, tmp, tmp) = self.inports[0]
        (x1, y1, tmp, tmp) = self.outports[0]



        IDTcell = _metalIDTFingers(
            name=self.name + "_IDT1",
            width=self.slabSingleLength - 2.0*config.dfIDTpitch,
            fingerwidth=config.dfIDTwidth,
            pitch=config.dfIDTpitch,
            n=self.IDTn,
            connectwidth=config.dfIDTpitch,
            connectionLength=self.slabWidth - self.IDToffset + config.dfOpeningWidth*1.5,
            metallayer=self.metallayer
        )

        IDTpatterns = []

        # IDT
        IDTx = float(x0 + (self.SAWresconatorConnection + self.slabSingleLength) / 2.0)
        IDTy = y0 - self.IDToffset

        IDTpatterns.append(gdspy.CellReference(IDTcell, (IDTx, IDTy), rotation=180.0))

        IDTx = float(x0 + 1.0*self.slabSingleLength + (self.SAWresconatorConnection + self.slabSingleLength) / 2.0)
        IDTy = y0 - self.IDToffset

        IDTpatterns.append(gdspy.CellReference(IDTcell, (IDTx, IDTy), rotation=0.0, x_reflection=True))

        IDTx = float(x0 + 2.0*self.slabSingleLength + (self.SAWresconatorConnection + self.slabSingleLength) / 2.0)
        IDTy = y0 - self.IDToffset

        IDTpatterns.append(gdspy.CellReference(IDTcell, (IDTx, IDTy), rotation=180.0))

        IDTx = float(x0 + 3.0*self.slabSingleLength + (self.SAWresconatorConnection + self.slabSingleLength) / 2.0)
        IDTy = y0 - self.IDToffset

        IDTpatterns.append(gdspy.CellReference(IDTcell, (IDTx, IDTy), rotation=0.0, x_reflection=True))

        # add IDT pads below. GSG pade
        padx = x0 + 2.0*self.slabSingleLength+ 0.5*self.SAWresconatorConnection
        pady = y0 - self.slabWidth - 30.0
        IDTpadG1 = gdspy.Rectangle((padx - config.dfIDTpadSize / 2.0 - config.dfIDTpadPitch , pady),
                                   (padx + config.dfIDTpadSize / 2.0 - config.dfIDTpadPitch, pady - config.dfIDTpadSize),
                                   layer=self.metallayer)
        IDTpadG2 = gdspy.Rectangle((padx - config.dfIDTpadSize / 2.0 + config.dfIDTpadPitch, pady ),
                                  (padx + config.dfIDTpadSize / 2.0 + config.dfIDTpadPitch, pady  - config.dfIDTpadSize),
                                  layer=self.metallayer)
        IDTpadS = gdspy.Rectangle((padx - config.dfIDTpadSize / 2.0, pady ),
                                   (padx + config.dfIDTpadSize / 2.0, pady - config.dfIDTpadSize),
                                   layer=self.metallayer)
        IDTpatterns.extend([IDTpadS, IDTpadG1, IDTpadG2])

        #connections
        #Ground
        pathGnd1 = [(x0 + 1.0*self.slabSingleLength + self.SAWresconatorConnection/2, y0 - self.slabWidth  - config.dfOpeningWidth ),
                 (x0 + 1.0*self.slabSingleLength + self.SAWresconatorConnection/2, pady - config.dfIDTLongWiring),
                 (padx - config.dfIDTpadPitch - 0.012564, pady - config.dfIDTLongWiring)
                 ]
        link2padcell = gdspy.PolyPath(pathGnd1, config.dfIDTLongWiring, layer=self.metallayer)
        IDTpatterns.append(link2padcell)

        pathGnd2 = [(x0 + 3.0*self.slabSingleLength + self.SAWresconatorConnection/2, y0 - self.slabWidth  - config.dfOpeningWidth ),
                 (x0 + 3.0*self.slabSingleLength + self.SAWresconatorConnection/2, pady - config.dfIDTLongWiring),
                 (padx + config.dfIDTpadPitch + 0.012564, pady - config.dfIDTLongWiring)
                 ]
        link2padcel2 = gdspy.PolyPath(pathGnd2, config.dfIDTLongWiring, layer=self.metallayer)
        IDTpatterns.append(link2padcel2)

        #Signal
        pathSig1 = [(x0 + 2.0*self.slabSingleLength + self.SAWresconatorConnection/2, y0 - self.slabWidth  - config.dfOpeningWidth ),
                 (x0 + 2.0*self.slabSingleLength + self.SAWresconatorConnection/2, pady - config.dfIDTLongWiring),

                 ]
        link2padcel3 = gdspy.PolyPath(pathSig1, config.dfIDTLongWiring, layer=self.metallayer)
        IDTpatterns.append(link2padcel3)


        #Signal-- Far end
        pathSig3 = [(x0 + 0.0 * self.slabSingleLength + self.SAWresconatorConnection / 2, y0 - self.slabWidth - config.dfOpeningWidth),
                    (x0 + 0.0 * self.slabSingleLength + self.SAWresconatorConnection / 2, pady - config.dfIDTpadSize*1.7),
                    (x0 + 4.0 * self.slabSingleLength + self.SAWresconatorConnection / 2, pady - config.dfIDTpadSize * 1.7),
                    (x0 + 4.0 * self.slabSingleLength + self.SAWresconatorConnection / 2, y0 - self.slabWidth - config.dfOpeningWidth),
                    ]
        link2padcel5 = gdspy.PolyPath(pathSig3, config.dfIDTLongWiring, layer=self.metallayer)
        IDTpatterns.append(link2padcel5)
        #
        pathSig4 = [(padx, pady - config.dfIDTpadSize),
                    (padx, pady - config.dfIDTpadSize * 1.7),
                    ]
        link2padcel6 = gdspy.PolyPath(pathSig4, config.dfIDTLongWiring, layer=self.metallayer)
        IDTpatterns.append(link2padcel6)

        combined = gdspy.fast_boolean(IDTpatterns, None, "or", layer=self.metallayer)
        self.add(combined)
        pass










class AcoustoOptStraightLongWaveguide(OptStraightWaveguide):
    """

    """
    suslayer = 20
    metallayer = 30
    slabSingleLength = 0.0
    slabWidth = 0.0
    slabN = 7
    IDToffset = 0.0
    IDTn = 0
    SAWresconatorConnection = 3.0
    def __init__(self, name, inports, slabSingleLength, slabWidth, IDToffset, IDTn, layer=10, suslayer = 20, metallayer = 30):
        self.slabN = 7
        self.SAWresconatorConnection = 3.0

        OptStraightWaveguide.__init__(self, name, inports, slabSingleLength*self.slabN + self.SAWresconatorConnection, layer)

        self.suslayer = suslayer
        self.metallayer = metallayer
        self.slabSingleLength = slabSingleLength
        self.slabWidth = slabWidth
        self.IDToffset = IDToffset
        self.IDTn = IDTn
        self.createIDT()
        self.createSuspendingOpening()

    def createSuspendingOpening(self):
        # top opening
        (x0, y0, tmp, tmp) = self.inports[0]
        for i in range(0,self.slabN):
            topopenOne = gdspy.Rectangle( (x0+self.SAWresconatorConnection, y0+config.dfOpeningOffset ),
                                   (x0 + self.slabSingleLength, y0 + config.dfOpeningOffset+1.5*config.dfOpeningWidth),
                                   layer=self.suslayer)
            x0 += self.slabSingleLength
            self.add([topopenOne])

        # bottom opening
        (x0, y0, tmp, tmp) = self.inports[0]
        for i in range(0,self.slabN):
            bottomopenOne = gdspy.Rectangle((x0 + self.SAWresconatorConnection, y0+config.dfOpeningOffset - self.slabWidth),
                                     (x0+self.slabSingleLength, y0 + config.dfOpeningOffset - self.slabWidth-1.5*config.dfOpeningWidth) ,
                                     layer=self.suslayer)
            x0 += self.slabSingleLength
            self.add([bottomopenOne])

        #left opening
        (x0, y0, tmp, tmp) = self.inports[0]
        leftopen = gdspy.Rectangle((x0-config.dfOpeningConnection, y0 - config.dfOpeningOffset ),
                                     (x0, y0 + config.dfOpeningOffset - self.slabWidth -  1.0*config.dfOpeningOffset) ,
                                     layer=self.suslayer)

        #right opening
        (x1, y1, tmp, tmp) = self.outports[0]
        rightopen = gdspy.Rectangle((x1 , y1 - config.dfOpeningOffset ),
                                     (x1 + config.dfOpeningConnection, y1 + config.dfOpeningOffset - self.slabWidth - 1.0*config.dfOpeningOffset) ,
                                     layer=self.suslayer)

        self.add([leftopen, rightopen])
        pass

    def createIDT(self):
        (x0, y0, tmp, tmp) = self.inports[0]
        (x1, y1, tmp, tmp) = self.outports[0]



        IDTcell = _metalIDTFingers(
            name=self.name + "_IDT1",
            width=self.slabSingleLength - 2.0*config.dfIDTpitch,
            fingerwidth=config.dfIDTwidth,
            pitch=config.dfIDTpitch,
            n=self.IDTn,
            connectwidth=config.dfIDTpitch,
            connectionLength=self.slabWidth - self.IDToffset + config.dfOpeningWidth*1.5,
            metallayer=self.metallayer
        )

        IDTpatterns = []

        # IDT#1
        IDTx = float(x0 + self.slabSingleLength + (self.SAWresconatorConnection + self.slabSingleLength) / 2.0)
        IDTy = y0 - self.IDToffset

        IDTpatterns.append(gdspy.CellReference(IDTcell, (IDTx, IDTy), rotation=180.0))

        IDTx = float(x0 + 2.0*self.slabSingleLength + (self.SAWresconatorConnection + self.slabSingleLength) / 2.0)
        IDTy = y0 - self.IDToffset

        IDTpatterns.append(gdspy.CellReference(IDTcell, (IDTx, IDTy), rotation=0.0, x_reflection=True))

        IDTx = float(x0 + 4.0*self.slabSingleLength + (self.SAWresconatorConnection + self.slabSingleLength) / 2.0)
        IDTy = y0 - self.IDToffset

        IDTpatterns.append(gdspy.CellReference(IDTcell, (IDTx, IDTy), rotation=180.0))

        IDTx = float(x0 + 5.0*self.slabSingleLength + (self.SAWresconatorConnection + self.slabSingleLength) / 2.0)
        IDTy = y0 - self.IDToffset

        IDTpatterns.append(gdspy.CellReference(IDTcell, (IDTx, IDTy), rotation=0.0, x_reflection=True))

        # add IDT pads below. GSG pade
        padx = x0 + 3.5*self.slabSingleLength+ 0.5*self.SAWresconatorConnection
        pady = y0 - self.slabWidth - 30.0
        IDTpadG1 = gdspy.Rectangle((padx - config.dfIDTpadSize / 2.0 - config.dfIDTpadPitch , pady),
                                   (padx + config.dfIDTpadSize / 2.0 - config.dfIDTpadPitch, pady - config.dfIDTpadSize),
                                   layer=self.metallayer)
        IDTpadG2 = gdspy.Rectangle((padx - config.dfIDTpadSize / 2.0 + config.dfIDTpadPitch, pady ),
                                  (padx + config.dfIDTpadSize / 2.0 + config.dfIDTpadPitch, pady  - config.dfIDTpadSize),
                                  layer=self.metallayer)
        IDTpadS = gdspy.Rectangle((padx - config.dfIDTpadSize / 2.0, pady ),
                                   (padx + config.dfIDTpadSize / 2.0, pady - config.dfIDTpadSize),
                                   layer=self.metallayer)
        IDTpatterns.extend([IDTpadS, IDTpadG1, IDTpadG2])

        #connections
        #Ground
        pathGnd1 = [(x0 + 2.0*self.slabSingleLength + self.SAWresconatorConnection/2, y0 - self.slabWidth  - config.dfOpeningWidth ),
                 (x0 + 2.0*self.slabSingleLength + self.SAWresconatorConnection/2, pady - config.dfIDTLongWiring),
                 (padx - config.dfIDTpadPitch, pady - config.dfIDTLongWiring)
                 ]
        link2padcell = gdspy.PolyPath(pathGnd1, config.dfIDTLongWiring, layer=self.metallayer)
        IDTpatterns.append(link2padcell)

        pathGnd2 = [(x0 + 5.0*self.slabSingleLength + self.SAWresconatorConnection/2, y0 - self.slabWidth  - config.dfOpeningWidth ),
                 (x0 + 5.0*self.slabSingleLength + self.SAWresconatorConnection/2, pady - config.dfIDTLongWiring),
                 (padx + config.dfIDTpadPitch, pady - config.dfIDTLongWiring)
                 ]
        link2padcel2 = gdspy.PolyPath(pathGnd2, config.dfIDTLongWiring, layer=self.metallayer)
        IDTpatterns.append(link2padcel2)

        #Signal
        pathSig1 = [(x0 + 3.0*self.slabSingleLength + self.SAWresconatorConnection/2, y0 - self.slabWidth  - config.dfOpeningWidth ),
                 (x0 + 3.0*self.slabSingleLength + self.SAWresconatorConnection/2, pady - config.dfIDTLongWiring),
                 (padx, pady - config.dfIDTLongWiring)
                 ]
        link2padcel3 = gdspy.PolyPath(pathSig1, config.dfIDTLongWiring, layer=self.metallayer)
        IDTpatterns.append(link2padcel3)

        pathSig2 = [(x0 + 4.0 * self.slabSingleLength + self.SAWresconatorConnection / 2, y0 - self.slabWidth - config.dfOpeningWidth),
                    (x0 + 4.0 * self.slabSingleLength + self.SAWresconatorConnection / 2, pady - config.dfIDTLongWiring),
                    (padx, pady - config.dfIDTLongWiring)
                    ]
        link2padcel4 = gdspy.PolyPath(pathSig2, config.dfIDTLongWiring, layer=self.metallayer)
        IDTpatterns.append(link2padcel4)

        #Signal-- Far end
        pathSig3 = [(x0 + 1.0 * self.slabSingleLength + self.SAWresconatorConnection / 2, y0 - self.slabWidth - config.dfOpeningWidth),
                    (x0 + 1.0 * self.slabSingleLength + self.SAWresconatorConnection / 2, pady - config.dfIDTpadSize*1.7),
                    (x0 + 6.0 * self.slabSingleLength + self.SAWresconatorConnection / 2, pady - config.dfIDTpadSize * 1.7),
                    (x0 + 6.0 * self.slabSingleLength + self.SAWresconatorConnection / 2, y0 - self.slabWidth - config.dfOpeningWidth),
                    ]
        link2padcel5 = gdspy.PolyPath(pathSig3, config.dfIDTLongWiring, layer=self.metallayer)
        IDTpatterns.append(link2padcel5)

        pathSig4 = [(padx, pady - config.dfIDTpadSize),
                    (padx, pady - config.dfIDTpadSize * 1.7),
                    ]
        link2padcel6 = gdspy.PolyPath(pathSig4, config.dfIDTLongWiring, layer=self.metallayer)
        IDTpatterns.append(link2padcel6)

        combined = gdspy.fast_boolean(IDTpatterns, None, "or", layer=self.metallayer)
        self.add(combined)
        pass






class AcoustoOptStraightWaveguide(OptStraightWaveguide):
    """

    """
    suslayer = 20
    metallayer = 30
    slabLength = 0.0
    slabWidth = 0.0
    IDToffset = 0.0
    IDTn = 0

    def __init__(self, name, inports, slabLength, slabWidth, IDToffset, IDTn, layer=10, suslayer = 20, metallayer = 30):
        OptStraightWaveguide.__init__(self, name, inports, slabLength + 4.0*config.dfOpeningWidth + 2.0*config.dfOpeningConnection, layer)
        self.suslayer = suslayer
        self.metallayer = metallayer
        self.slabLength = slabLength
        self.slabWidth = slabWidth
        self.IDToffset = IDToffset
        self.IDTn = IDTn
        self.createIDT()
        self.createSuspendingOpening()

    def createSuspendingOpening(self):
        # top opening
        (x0, y0, tmp, tmp) = self.inports[0]
        (x1, y1, tmp, tmp) = self.outports[0]
        topopen = gdspy.Rectangle( (x0+config.dfOpeningConnection, y0+config.dfOpeningOffset ),
                                   (x1-config.dfOpeningConnection, y0 + config.dfOpeningOffset+1.5*config.dfOpeningWidth),
                                   layer=self.suslayer)

        # bottom opening
        bottomopen = gdspy.Rectangle((x0, y0+config.dfOpeningOffset - self.slabWidth),
                                     (x1, y0 + config.dfOpeningOffset - self.slabWidth-1.5*config.dfOpeningWidth) ,
                                     layer=self.suslayer)

        #left opening
        leftopen = gdspy.Rectangle((x0+config.dfOpeningConnection, y0 - config.dfOpeningOffset ),
                                     (x0 + config.dfOpeningConnection+ 2.0*config.dfOpeningWidth, y0 + config.dfOpeningOffset - self.slabWidth+ 2.0*config.dfOpeningOffset) ,
                                     layer=self.suslayer)

        #right opening
        rightopen = gdspy.Rectangle((x1-config.dfOpeningConnection, y1 - config.dfOpeningOffset ),
                                     (x1 - config.dfOpeningConnection- 2.0*config.dfOpeningWidth, y1 + config.dfOpeningOffset - self.slabWidth+ 2.0*config.dfOpeningOffset) ,
                                     layer=self.suslayer)

        self.add([topopen,bottomopen, leftopen, rightopen])
        pass

    def createIDT(self):
        (x0, y0, tmp, tmp) = self.inports[0]
        (x1, y1, tmp, tmp) = self.outports[0]
        IDTx = float(x0 + x1) / 2.0
        IDTy = y0 - self.IDToffset

        IDTcell = _metalIDTFingers(
            name=self.name + "_IDT1",
            width=self.slabLength - config.dfOpeningOffset * 2.0,
            fingerwidth=config.dfIDTwidth,
            pitch=config.dfIDTpitch,
            n=self.IDTn,
            connectwidth=config.dfIDTpitch,
            connectionLength=self.slabWidth - self.IDToffset - config.dfOpeningOffset - 1.0 * config.dfIDTpitch,
            metallayer=self.metallayer
        )
        self.add(gdspy.CellReference(IDTcell, (IDTx, IDTy), rotation=180.0))

        # add IDT pads below.
        IDTpad1 = gdspy.Rectangle((IDTx - config.dfIDTpadSize / 2.0 - config.dfIDTpadPitch / 2.0, IDTy - 4 * self.slabWidth),
                                  (IDTx + config.dfIDTpadSize / 2.0 - config.dfIDTpadPitch / 2.0, IDTy - 4 * self.slabWidth - config.dfIDTpadSize),
                                  layer=self.metallayer)
        IDTpad2 = gdspy.Rectangle((IDTx - config.dfIDTpadSize / 2.0 + config.dfIDTpadPitch / 2.0, IDTy - 4 * self.slabWidth),
                                  (IDTx + config.dfIDTpadSize / 2.0 + config.dfIDTpadPitch / 2.0, IDTy - 4 * self.slabWidth - config.dfIDTpadSize),
                                  layer=self.metallayer)
        # self.add([IDTpad1, IDTpad2])

        connectionOffset = min(1.2, config.dfIDTpitch)

        # draw connections
        xleftjoint = IDTx - self.slabLength / 2.0 - 2.0 * config.dfOpeningWidth - 2.0 * config.dfOpeningConnection
        yleftjoint = y0 + config.dfOpeningOffset - self.slabWidth + 2.5 * connectionOffset

        xrightjoint = IDTx + self.slabLength / 2.0 + 2.0 * config.dfOpeningWidth + 2.0 * config.dfOpeningConnection
        yrightjoint = y0 + config.dfOpeningOffset - self.slabWidth + 2.5 * connectionOffset

        extendlink1 = gdspy.Rectangle((IDTx - self.slabLength / 2.0 + config.dfOpeningOffset - config.dfIDTpitch / 2.0,
                                       y0 + config.dfOpeningOffset - self.slabWidth + 1.0 * connectionOffset),
                                      (xleftjoint, yleftjoint), layer=self.metallayer)
        extendlink2 = gdspy.Rectangle((IDTx + self.slabLength / 2.0 - config.dfOpeningOffset + config.dfIDTpitch / 2.0,
                                       y0 + config.dfOpeningOffset - self.slabWidth + 1.0 * connectionOffset),
                                      (xrightjoint, yrightjoint), layer=self.metallayer)
        link2Pad1 = [(xleftjoint - config.dfIDTLongWiring / 2.0, yleftjoint),
                     (xleftjoint - config.dfIDTLongWiring / 2.0, IDTy - 4 * self.slabWidth - config.dfIDTLongWiring / 2.0),
                     (IDTx - config.dfIDTpadPitch / 2.0, IDTy - 4 * self.slabWidth - config.dfIDTLongWiring / 2.0), ]
        link2Pad2 = [(xrightjoint + config.dfIDTLongWiring / 2.0, yrightjoint),
                     (xrightjoint + config.dfIDTLongWiring / 2.0, IDTy - 4 * self.slabWidth - config.dfIDTLongWiring / 2.0),
                     (IDTx + config.dfIDTpadPitch / 2.0, IDTy - 4 * self.slabWidth - config.dfIDTLongWiring / 2.0), ]
        link2padcell = gdspy.PolyPath(link2Pad1, config.dfIDTLongWiring, layer=self.metallayer)
        link2padcel2 = gdspy.PolyPath(link2Pad2, config.dfIDTLongWiring, layer=self.metallayer)

        combined = gdspy.fast_boolean([extendlink1, extendlink2, link2padcell, link2padcel2, IDTpad1, IDTpad2], None, "or", layer=self.metallayer)
        self.add(combined)

        pass


class AcoustoOptSuspendedOptRaceTrackCavityVC(OptRaceTrackCavityVC):
    """

    """
    suslayer = 20
    metallayer = 30
    slabLength = 0.0
    slabWidth = 0.0
    IDToffset = 0.0
    IDTn = 0
    def __init__(self, name, inport, cavityradius, cavityRacinglength, couplinggap, slabLength,  slabWidth, IDToffset, IDTn,
                 layer=10, direction=-1, suslayer=20, metallayer=30):
        OptRaceTrackCavityVC.__init__(self, name, inport, cavityradius, cavityRacinglength, couplinggap, layer, direction)
        self.suslayer = suslayer
        self.metallayer = metallayer
        self.slabLength = slabLength
        self.slabWidth = slabWidth
        self.IDToffset = IDToffset
        self.IDTn = IDTn
        if slabLength > cavityRacinglength - 3*config.dfOpeningOffset:
            warnings.warn("[OptHedgehog WARNING] the SAW interaction length is shorter than the straight region of cavity.")

        self.createSuspendingOpening()
        self.createSuspendingOpenWG()
        self.createIDT()

    def createSuspendingOpenWG(self):
        couplingSuspend = _createsuspath(self.pathnodes, self.suslayer)
        cavitySuspended = _createsuspath(self.pathcavity, self.suslayer)

        #create fab waveguide path to do the boolean operation
        fatwg1 = gdspy.PolyPath(self.pathnodes, width=2*config.dfOpeningOffset, max_points=199, layer=0, corners=1)
        fatwg2 = gdspy.PolyPath(self.pathcavity, width=2 * config.dfOpeningOffset, max_points=199, layer=0, corners=1)
        xmid = (self.xleftcenter + self.xrightcenter) / 2.0
        x0 = xmid - self.slabLength / 2.0 - 2.0 * config.dfOpeningWidth - config.dfOpeningConnection
        y0 = self.yleftcenter - self.cavityradius + 2.0* config.dfOpeningOffset + 2.0 * config.dfOpeningWidth
        x1 = xmid + self.slabLength / 2.0 + 2.0 * config.dfOpeningWidth + config.dfOpeningConnection
        y1 = self.yleftcenter - self.cavityradius - self.slabWidth - 2.0 * config.dfOpeningOffset + 2.0 * config.dfOpeningWidth
        fatSAWregion = gdspy.Rectangle( (x0, y0), (x1, y1))            # SAW region
        fatwgTot = gdspy.fast_boolean(fatwg1, fatwg2, "or", precision= 0.01)
        fatwgTot = gdspy.fast_boolean(fatwgTot, fatSAWregion, "or", precision= 0.01)
        #
        couplingSuspend = gdspy.fast_boolean(couplingSuspend,fatwgTot, "not", layer = self.suslayer, precision= 0.01)
        cavitySuspended = gdspy.fast_boolean(cavitySuspended,fatwgTot, "not", layer = self.suslayer, precision= 0.01)

        self.add(couplingSuspend)
        self.add(cavitySuspended)

        pass


    def createSuspendingOpening(self):
        #create openings for SAW part
        xmid = (self.xleftcenter + self.xrightcenter) / 2.0
        x0 = xmid - self.slabLength/2.0 - 2.0* config.dfOpeningWidth - config.dfOpeningConnection
        y0 = self.yleftcenter - self.cavityradius
        x1 = xmid + self.slabLength/2.0 + 2.0* config.dfOpeningWidth + config.dfOpeningConnection
        y1 = self.yrightcenter - self.cavityradius

        # reuse the code from straight waveguide w/ IDT

        # top opening
        topopen = gdspy.Rectangle( (x0+config.dfOpeningConnection, y0+config.dfOpeningOffset ),
                                   (x1-config.dfOpeningConnection, y0 + config.dfOpeningOffset+1.5*config.dfOpeningWidth),
                                   layer=self.suslayer)

        # bottom opening
        bottomopen = gdspy.Rectangle((x0, y0+config.dfOpeningOffset - self.slabWidth),
                                     (x1, y0 + config.dfOpeningOffset - self.slabWidth-1.5*config.dfOpeningWidth) ,
                                     layer=self.suslayer)

        #left opening
        leftopen = gdspy.Rectangle((x0+config.dfOpeningConnection, y0 - config.dfOpeningOffset ),
                                     (x0 + config.dfOpeningConnection+ 2.0*config.dfOpeningWidth, y0 + config.dfOpeningOffset - self.slabWidth+ 2.0*config.dfOpeningOffset) ,
                                     layer=self.suslayer)

        #right opening
        rightopen = gdspy.Rectangle((x1-config.dfOpeningConnection, y1 - config.dfOpeningOffset ),
                                     (x1 - config.dfOpeningConnection- 2.0*config.dfOpeningWidth, y1 + config.dfOpeningOffset - self.slabWidth+ 2.0*config.dfOpeningOffset) ,
                                     layer=self.suslayer)

        self.add([topopen,bottomopen, leftopen, rightopen])
        pass

    def createIDT(self):
        x0 = self.xleftcenter
        y0 = self.yleftcenter - self.cavityradius
        x1 = self.xrightcenter
        y1 = self.yrightcenter - self.cavityradius

        # reuse the code from straight waveguide IDT
        IDTx = float(x0 + x1) / 2.0
        IDTy = y0 - self.IDToffset

        IDTcell = _metalIDTFingers(
            name = self.name+"_IDT1",
            width = self.slabLength - config.dfOpeningOffset*3.0,
            fingerwidth = config.dfIDTwidth,
            pitch = config.dfIDTpitch,
            n = self.IDTn,
            connectwidth= config.dfIDTpitch,
            connectionLength= self.slabWidth - self.IDToffset - config.dfOpeningOffset - 0.5*config.dfOpeningOffset,
            metallayer= self.metallayer
        )
        self.add(gdspy.CellReference(IDTcell, (IDTx, IDTy), rotation=180.0))

        # add IDT pads below.
        IDTpad1 = gdspy.Rectangle(  (IDTx - config.dfIDTpadSize/2.0 - config.dfIDTpadPitch/2.0, IDTy - 4*self.slabWidth),
                                    (IDTx + config.dfIDTpadSize/2.0 - config.dfIDTpadPitch/2.0, IDTy - 4*self.slabWidth - config.dfIDTpadSize),
                                    layer = self.metallayer)
        IDTpad2 = gdspy.Rectangle((IDTx - config.dfIDTpadSize / 2.0 + config.dfIDTpadPitch/2.0, IDTy - 4 * self.slabWidth),
                                  (IDTx + config.dfIDTpadSize / 2.0 + config.dfIDTpadPitch/2.0, IDTy - 4 * self.slabWidth - config.dfIDTpadSize),
                                  layer=self.metallayer)
        #self.add([IDTpad1, IDTpad2])

        #draw connections
        xleftjoint = IDTx - self.slabLength / 2.0 - 2.0 * config.dfOpeningWidth - 2.0 * config.dfOpeningConnection
        yleftjoint = y0 + config.dfOpeningOffset - self.slabWidth + 1.5 * config.dfOpeningOffset

        xrightjoint = IDTx + self.slabLength / 2.0 + 2.0 * config.dfOpeningWidth + 2.0 * config.dfOpeningConnection
        yrightjoint = y0 + config.dfOpeningOffset - self.slabWidth + 1.5 * config.dfOpeningOffset


        extendlink1 = gdspy.Rectangle( (IDTx - self.slabLength/2.0 + config.dfOpeningOffset, y0 + config.dfOpeningOffset - self.slabWidth + 0.5*config.dfOpeningOffset),
                                       ( xleftjoint, yleftjoint), layer= self.metallayer)
        extendlink2 = gdspy.Rectangle( (IDTx + self.slabLength/2.0 - config.dfOpeningOffset, y0 + config.dfOpeningOffset - self.slabWidth + 0.5*config.dfOpeningOffset),
                                       ( xrightjoint, yrightjoint), layer= self.metallayer)
        link2Pad1 = [ (xleftjoint - config.dfIDTLongWiring/2.0 , yleftjoint ),
                     (xleftjoint - config.dfIDTLongWiring/2.0 , IDTy - 4*self.slabWidth - config.dfIDTLongWiring/2.0 ),
                     ( IDTx - config.dfIDTpadPitch/2.0, IDTy - 4*self.slabWidth - config.dfIDTLongWiring/2.0 ),]
        link2Pad2 = [(xrightjoint + config.dfIDTLongWiring / 2.0, yrightjoint),
                    (xrightjoint + config.dfIDTLongWiring / 2.0, IDTy - 4 * self.slabWidth - config.dfIDTLongWiring / 2.0),
                    (IDTx + config.dfIDTpadPitch / 2.0, IDTy - 4 * self.slabWidth - config.dfIDTLongWiring / 2.0), ]
        link2padcell = gdspy.PolyPath(link2Pad1, config.dfIDTLongWiring, layer = self.metallayer)
        link2padcel2 = gdspy.PolyPath(link2Pad2, config.dfIDTLongWiring, layer=self.metallayer)

        combined = gdspy.fast_boolean([extendlink1, extendlink2, link2padcell, link2padcel2, IDTpad1, IDTpad2], None, "or", layer = self.metallayer)
        self.add(combined)



class AcoustoOptSusCoupledRaceTrack(OptCoupledRaceTrack):
    """

    """
    suslayer = 20
    metallayer = 30
    slabLength = 0.0
    slabWidth = 0.0
    IDToffset = 0.0
    IDTn = 0
    protected = []

    def __init__(self, name, inport, cavityradius, cavityRacinglength, WGcplGap, cavitycplGap, ringwidth=config.dfoptwgwidth, layer=10,
                 slabLength=90.0, slabWidth=13.0, IDToffset = 2.25, IDTn = 4, suslayer = 20, metallayer = 30):
        OptCoupledRaceTrack.__init__(self, name, inport, cavityradius, cavityRacinglength, WGcplGap, cavitycplGap, ringwidth, layer)
        self.suslayer = suslayer
        self.metallayer = metallayer
        self.slabLength = slabLength
        self.slabWidth = slabWidth
        self.IDToffset = IDToffset
        self.IDTn = IDTn
        if slabLength > cavityRacinglength - 3*config.dfOpeningOffset:
            warnings.warn("[OptHedgehog WARNING] the SAW interaction length is shorter than the straight region of cavity.")

        self.createIDT()
        self.createBiasElectrodes()
        self.createSuspendingOpening()
        pass

    def createIDT(self):
        x0 = self.cavity2L[0]
        y0 = self.cavity2L[1] - self.cavityradius
        x1 = self.cavity2R[0]
        y1 = self.cavity2L[1] - self.cavityradius

        # reuse the code from straight waveguide IDT
        IDTx = float(x0 + x1) / 2.0
        IDTy = y0 - self.IDToffset - self.CavitycplGap

        IDTcell = _metalIDTFingers(
            name = self.name+"_IDT1",
            width = self.slabLength - config.dfOpeningOffset*2.0,
            fingerwidth = config.dfIDTwidth,
            pitch = config.dfIDTpitch,
            n = self.IDTn,
            connectwidth= config.dfIDTpitch,
            connectionLength= self.slabWidth - self.IDToffset - self.CavitycplGap - config.dfOpeningOffset - 1.0*config.dfIDTpitch,
            metallayer= self.metallayer
        )
        self.add(gdspy.CellReference(IDTcell, (IDTx, IDTy), rotation=180.0))

        # add IDT pads below.
        IDTpad1 = gdspy.Rectangle(  (IDTx - config.dfIDTpadSize/2.0 - config.dfIDTpadPitch/2.0, IDTy - 4*self.slabWidth),
                                    (IDTx + config.dfIDTpadSize/2.0 - config.dfIDTpadPitch/2.0, IDTy - 4*self.slabWidth - config.dfIDTpadSize),
                                    layer = self.metallayer)
        IDTpad2 = gdspy.Rectangle((IDTx - config.dfIDTpadSize / 2.0 + config.dfIDTpadPitch/2.0, IDTy - 4 * self.slabWidth),
                                  (IDTx + config.dfIDTpadSize / 2.0 + config.dfIDTpadPitch/2.0, IDTy - 4 * self.slabWidth - config.dfIDTpadSize),
                                  layer=self.metallayer)
        #self.add([IDTpad1, IDTpad2])

        #draw connections
        xleftjoint = IDTx - self.slabLength / 2.0 - 2.0 * config.dfOpeningWidth - 2.0 * config.dfOpeningConnection
        yleftjoint = y0 + config.dfOpeningOffset - self.slabWidth + 2.5 * config.dfIDTpitch

        xrightjoint = IDTx + self.slabLength / 2.0 + 2.0 * config.dfOpeningWidth + 2.0 * config.dfOpeningConnection
        yrightjoint = y0 + config.dfOpeningOffset - self.slabWidth + 2.5 * config.dfIDTpitch


        extendlink1 = gdspy.Rectangle( (IDTx - self.slabLength/2.0 + config.dfOpeningOffset - config.dfIDTpitch/2.0, y0 + config.dfOpeningOffset - self.slabWidth + 1.0*config.dfIDTpitch),
                                       ( xleftjoint, yleftjoint), layer= self.metallayer)
        extendlink2 = gdspy.Rectangle( (IDTx + self.slabLength/2.0 - config.dfOpeningOffset + config.dfIDTpitch/2.0, y0 + config.dfOpeningOffset - self.slabWidth + 1.0*config.dfIDTpitch),
                                       ( xrightjoint, yrightjoint), layer= self.metallayer)
        link2Pad1 = [ (xleftjoint - config.dfIDTLongWiring/2.0 , yleftjoint ),
                     (xleftjoint - config.dfIDTLongWiring/2.0 , IDTy - 4*self.slabWidth - config.dfIDTLongWiring/2.0 ),
                     ( IDTx - config.dfIDTpadPitch/2.0, IDTy - 4*self.slabWidth - config.dfIDTLongWiring/2.0 ),]
        link2Pad2 = [(xrightjoint + config.dfIDTLongWiring / 2.0, yrightjoint),
                    (xrightjoint + config.dfIDTLongWiring / 2.0, IDTy - 4 * self.slabWidth - config.dfIDTLongWiring / 2.0),
                    (IDTx + config.dfIDTpadPitch / 2.0, IDTy - 4 * self.slabWidth - config.dfIDTLongWiring / 2.0), ]
        link2padcell = gdspy.PolyPath(link2Pad1, config.dfIDTLongWiring, layer = self.metallayer)
        link2padcel2 = gdspy.PolyPath(link2Pad2, config.dfIDTLongWiring, layer=self.metallayer)

        combined = gdspy.fast_boolean([extendlink1, extendlink2, link2padcell, link2padcel2, IDTpad1, IDTpad2], None, "or", layer = self.metallayer)
        self.add(combined)


    def createBiasElectrodes(self):
        x0 = self.cavity2L[0]
        y0 = self.cavity2L[1] + self.cavityradius
        x1 = self.cavity2R[0]
        y1 = self.cavity2L[1] + self.cavityradius
        offset = self.IDToffset

        #upper electrode
        upperelectrode = gdspy.Rectangle( (x0, y0 + offset), (x1, y1 + offset + config.dfBiasLongWiring), layer = self.metallayer)
        xup = 0.5*(x0 + x1)
        yup = y1 + offset + config.dfBiasLongWiring
        #lower electrode
        lowerelectrode = gdspy.Rectangle( (x0, y0 - offset), (x1, y1 - offset - config.dfBiasLongWiring), layer = self.metallayer)
        xdown = 0.5*(x0 + x1)
        ydown = y1 - offset - config.dfBiasLongWiring

        #left pad
        padLx = self.cavity2L[0] - self.cavityradius - config.dfIDTpadPitch/2.0
        padLy = self.cavity2L[1]
        padL = gdspy.Rectangle((padLx - config.dfBiaspadSize/2, padLy - config.dfBiaspadSize/2.0),
                               (padLx + config.dfBiaspadSize/2, padLy + config.dfBiaspadSize/2.0), layer=self.metallayer)

        #right pad
        padRx = self.cavity2L[0] - self.cavityradius + config.dfIDTpadPitch / 2.0
        padRy = self.cavity2L[1]
        padR = gdspy.Rectangle((padRx - config.dfBiaspadSize / 2, padRy - config.dfBiaspadSize / 2.0),
                               (padRx + config.dfBiaspadSize / 2, padRy + config.dfBiaspadSize / 2.0), layer=self.metallayer)

        #linkpadth
        linkpathup = [ (xup, yup), (xup, yup + 50.0), (padLx, yup+50.0), (padLx, padLy + config.dfBiaspadSize/2.0)]
        linkpathdown = [(xdown, ydown), (xdown, padRy), (padRx  + config.dfBiaspadSize / 2.0, padRy)]
        linkL = gdspy.PolyPath(linkpathup, width=config.dfBiasLongWiring, layer=self.metallayer)
        linkR = gdspy.PolyPath(linkpathdown, width=config.dfBiasLongWiring, layer=self.metallayer)

        merged = gdspy.fast_boolean([padL, padR, upperelectrode, lowerelectrode, linkL, linkR], None, "or", layer = self.metallayer)
        self.add(merged)
        pass

    def createSuspendingOpening(self):
        self.protected = []
        # create openings for SAW part
        xmid = (self.cavity2L[0] + self.cavity2R[0]) / 2.0
        x0 = xmid - self.slabLength / 2.0 - 2.0 * config.dfOpeningWidth - config.dfOpeningConnection
        y0 = self.cavity2L[1] - self.cavityradius
        x1 = xmid + self.slabLength / 2.0 + 2.0 * config.dfOpeningWidth + config.dfOpeningConnection
        y1 = self.cavity2R[1] - self.cavityradius

        zone = gdspy.Rectangle((x0, y0 + 3*config.dfOpeningOffset), (x1, y1 - self.CavitycplGap - 3.0*config.dfOpeningOffset), layer = 0)
        self.protected.append(zone)

        # top opening
        topopen = gdspy.Rectangle((x0 + config.dfOpeningConnection, y0 + config.dfOpeningOffset),
                                  (x1 - config.dfOpeningConnection, y0 + config.dfOpeningOffset + 1.5 * config.dfOpeningWidth),
                                  layer=self.suslayer)

        # bottom opening
        bottomopen = gdspy.Rectangle((x0, y0 + config.dfOpeningOffset - self.slabWidth),
                                     (x1, y0 + config.dfOpeningOffset - self.slabWidth - 1.5 * config.dfOpeningWidth),
                                     layer=self.suslayer)

        # left opening
        leftopen = gdspy.Rectangle((x0 + 0.5*config.dfOpeningConnection, y0 - config.dfOpeningOffset - self.CavitycplGap),
                                   (x0 + config.dfOpeningConnection + 2.0 * config.dfOpeningWidth,
                                    y0 + config.dfOpeningOffset - self.slabWidth + 3.5 * config.dfIDTpitch),
                                   layer=self.suslayer)

        # right opening
        rightopen = gdspy.Rectangle((x1 - 0.5*config.dfOpeningConnection, y1 - config.dfOpeningOffset - self.CavitycplGap),
                                    (x1 - config.dfOpeningConnection - 2.0 * config.dfOpeningWidth,
                                     y1 + config.dfOpeningOffset - self.slabWidth + 3.5 * config.dfIDTpitch),
                                    layer=self.suslayer)

        self.add([topopen, bottomopen, leftopen, rightopen])


        #create openting for Bias electrodes
        xmid = (self.cavity2L[0] + self.cavity2R[0]) / 2.0
        x0 = self.cavity2L[0]
        y0 = self.cavity2L[1] + self.cavityradius
        x1 = self.cavity2R[0]
        y1 = self.cavity2R[1] + self.cavityradius
        #for openings
        topleft = gdspy.Rectangle( (x0, y0 + config.dfBiasLongWiring + self.IDToffset + config.dfOpeningOffset/2.0),
                                   (xmid - config.dfBiasLongWiring/2.0 - config.dfOpeningOffset/2.0 , y1 + config.dfBiasLongWiring + self.IDToffset + 2*config.dfOpeningWidth),
                                   layer = self.suslayer)
        topright = gdspy.Rectangle( (x1, y1 + config.dfBiasLongWiring + self.IDToffset + config.dfOpeningOffset/2.0),
                                   (xmid + config.dfBiasLongWiring/2.0 + config.dfOpeningOffset/2.0 , y1 + config.dfBiasLongWiring + self.IDToffset + 2*config.dfOpeningWidth),
                                   layer = self.suslayer)
        btmleft = gdspy.Rectangle( (x0, y0 - config.dfBiasLongWiring - self.IDToffset - config.dfOpeningOffset/2.0),
                                   (xmid - config.dfBiasLongWiring/2.0 - config.dfOpeningOffset/2.0 , y1 - config.dfBiasLongWiring - self.IDToffset - 2*config.dfOpeningWidth),
                                   layer = self.suslayer)
        btmright = gdspy.Rectangle( (x1, y1 - config.dfBiasLongWiring - self.IDToffset - config.dfOpeningOffset/2.0),
                                   (xmid + config.dfBiasLongWiring/2.0 + config.dfOpeningOffset/2.0 , y1 - config.dfBiasLongWiring - self.IDToffset - 2*config.dfOpeningWidth),
                                   layer = self.suslayer)


        zone = gdspy.Rectangle((x0 - 0.5*config.dfOpeningConnection , y0 + 3 * config.dfOpeningOffset), (x1 + 0.5*config.dfOpeningConnection, y1 - 3.0 * config.dfOpeningOffset), layer=0)
        self.protected.append(zone)

        self.add([topleft, topright, btmleft, btmright])


        ## add opening for regular path
        openwg1 = _createsuspath(self.path_wg1, self.suslayer)
        openwg2 = _createsuspath(self.path_wg2, self.suslayer)
        opencavity1 = _createsuspath(self.path_cavity1, self.suslayer)
        opencavity2 = _createsuspath(self.path_cavity2, self.suslayer)

        fatwg1 = gdspy.PolyPath(self.path_wg1, width=2*config.dfOpeningOffset, max_points=199, layer=0, corners=1)
        fatwg2 = gdspy.PolyPath(self.path_wg2, width=2 * config.dfOpeningOffset, max_points=199, layer=0, corners=1)
        fatcavity1 = gdspy.PolyPath(self.path_cavity1, width=2 * config.dfOpeningOffset, max_points=199, layer=0, corners=1)
        fatcavity2 = gdspy.PolyPath(self.path_cavity2, width=2 * config.dfOpeningOffset, max_points=199, layer=0, corners=1)

        self.protected.extend([fatwg1, fatwg2, fatcavity1, fatcavity2])

        fatwgTot = gdspy.fast_boolean(self.protected, None, "or", precision= 0.05)
        openwg1 = gdspy.fast_boolean(openwg1, fatwgTot, "not", precision = 0.05, layer=self.suslayer)
        openwg2 = gdspy.fast_boolean(openwg2, fatwgTot, "not", precision=0.05, layer=self.suslayer)
        opencavity1 = gdspy.fast_boolean(opencavity1, fatwgTot, "not", precision = 0.05, layer=self.suslayer)
        opencavity2 = gdspy.fast_boolean(opencavity2, fatwgTot, "not", precision=0.05, layer=self.suslayer)


        self.add([openwg1, openwg2, opencavity1, opencavity2])

        pass


class AcoustoOptSusSingleRaceTrack(OptSingleEMAORaceTrack):
    """
        Reuse code from AcoustoOptSusCoupledRaceTrack
    """
    suslayer = 20
    metallayer = 30
    slabLength = 0.0
    slabWidth = 0.0
    IDToffset = 0.0
    IDTn = 0
    protected = []

    def __init__(self, name, inport, cavityradius, cavityRacinglength, WGcplGap, ringwidth=config.dfoptwgwidth, layer=10,
                 slabLength=90.0, slabWidth=13.0, IDToffset = 2.25, IDTn = 4, suslayer = 20, metallayer = 30):
        OptSingleEMAORaceTrack.__init__(self, name, inport, cavityradius, cavityRacinglength, WGcplGap, ringwidth, layer)
        self.suslayer = suslayer
        self.metallayer = metallayer
        self.slabLength = slabLength
        self.slabWidth = slabWidth
        self.IDToffset = IDToffset
        self.IDTn = IDTn
        if slabLength > cavityRacinglength - 3*config.dfOpeningOffset:
            warnings.warn("[OptHedgehog WARNING] the SAW interaction length is shorter than the straight region of cavity.")

        self.createIDT()
        self.createBiasElectrodes()
        self.createSuspendingOpening()
        pass

    def createIDT(self):
        x0 = self.cavity2L[0]
        y0 = self.cavity2L[1] - self.cavityradius
        x1 = self.cavity2R[0]
        y1 = self.cavity2L[1] - self.cavityradius

        # reuse the code from straight waveguide IDT
        IDTx = float(x0 + x1) / 2.0
        #IDTy = y0 - self.IDToffset - self.CavitycplGap
        IDTy = y0 - self.IDToffset # changed ... DO not need to consider gap...it's only one cavity...

        IDTcell = _metalIDTFingers(
            name = self.name+"_IDT1",
            width = self.slabLength - config.dfOpeningOffset*2.0,
            fingerwidth = config.dfIDTwidth,
            pitch = config.dfIDTpitch,
            n = self.IDTn,
            connectwidth= config.dfIDTpitch,
            connectionLength= self.slabWidth - self.IDToffset  - config.dfOpeningOffset - 1.0*config.dfIDTpitch,
            metallayer= self.metallayer
        )
        self.add(gdspy.CellReference(IDTcell, (IDTx, IDTy), rotation=180.0))

        # add IDT pads below.
        IDTpad1 = gdspy.Rectangle(  (IDTx - config.dfIDTpadSize/2.0 - config.dfIDTpadPitch/2.0, IDTy - 4*self.slabWidth),
                                    (IDTx + config.dfIDTpadSize/2.0 - config.dfIDTpadPitch/2.0, IDTy - 4*self.slabWidth - config.dfIDTpadSize),
                                    layer = self.metallayer)
        IDTpad2 = gdspy.Rectangle((IDTx - config.dfIDTpadSize / 2.0 + config.dfIDTpadPitch/2.0, IDTy - 4 * self.slabWidth),
                                  (IDTx + config.dfIDTpadSize / 2.0 + config.dfIDTpadPitch/2.0, IDTy - 4 * self.slabWidth - config.dfIDTpadSize),
                                  layer=self.metallayer)
        #self.add([IDTpad1, IDTpad2])

        connectionOffset = min(1.2, config.dfIDTpitch)

        #draw connections
        xleftjoint = IDTx - self.slabLength / 2.0 - 2.0 * config.dfOpeningWidth - 2.0 * config.dfOpeningConnection
        yleftjoint = y0 + config.dfOpeningOffset - self.slabWidth + 2.5 * connectionOffset

        xrightjoint = IDTx + self.slabLength / 2.0 + 2.0 * config.dfOpeningWidth + 2.0 * config.dfOpeningConnection
        yrightjoint = y0 + config.dfOpeningOffset - self.slabWidth + 2.5 * connectionOffset


        extendlink1 = gdspy.Rectangle( (IDTx - self.slabLength/2.0 + config.dfOpeningOffset - config.dfIDTpitch/2.0, y0 + config.dfOpeningOffset - self.slabWidth + 1.0*connectionOffset),
                                       ( xleftjoint, yleftjoint), layer= self.metallayer)
        extendlink2 = gdspy.Rectangle( (IDTx + self.slabLength/2.0 - config.dfOpeningOffset + config.dfIDTpitch/2.0, y0 + config.dfOpeningOffset - self.slabWidth + 1.0*connectionOffset),
                                       ( xrightjoint, yrightjoint), layer= self.metallayer)
        link2Pad1 = [ (xleftjoint - config.dfIDTLongWiring/2.0 , yleftjoint ),
                     (xleftjoint - config.dfIDTLongWiring/2.0 , IDTy - 4*self.slabWidth - config.dfIDTLongWiring/2.0 ),
                     ( IDTx - config.dfIDTpadPitch/2.0, IDTy - 4*self.slabWidth - config.dfIDTLongWiring/2.0 ),]
        link2Pad2 = [(xrightjoint + config.dfIDTLongWiring / 2.0, yrightjoint),
                    (xrightjoint + config.dfIDTLongWiring / 2.0, IDTy - 4 * self.slabWidth - config.dfIDTLongWiring / 2.0),
                    (IDTx + config.dfIDTpadPitch / 2.0, IDTy - 4 * self.slabWidth - config.dfIDTLongWiring / 2.0), ]
        link2padcell = gdspy.PolyPath(link2Pad1, config.dfIDTLongWiring, layer = self.metallayer)
        link2padcel2 = gdspy.PolyPath(link2Pad2, config.dfIDTLongWiring, layer=self.metallayer)

        combined = gdspy.fast_boolean([extendlink1, extendlink2, link2padcell, link2padcel2, IDTpad1, IDTpad2], None, "or", layer = self.metallayer)
        self.add(combined)


    def createBiasElectrodes(self):
        x0 = (self.cavity2L[0] + self.cavity2R[0])/2.0 - self.slabLength/2.0
        y0 = self.cavity2L[1] + self.cavityradius
        x1 = (self.cavity2L[0] + self.cavity2R[0])/2.0 + self.slabLength/2.0
        y1 = self.cavity2L[1] + self.cavityradius
        offset = self.IDToffset

        #upper electrode
        upperelectrode = gdspy.Rectangle( (x0, y0 + offset), (x1, y1 + offset + config.dfBiasLongWiring), layer = self.metallayer)
        xup = 0.5*(x0 + x1)
        yup = y1 + offset + config.dfBiasLongWiring
        #lower electrode
        lowerelectrode = gdspy.Rectangle( (x0, y0 - offset), (x1, y1 - offset - config.dfBiasLongWiring), layer = self.metallayer)
        xdown = 0.5*(x0 + x1)
        ydown = y1 - offset - config.dfBiasLongWiring

        #left pad
        padLx = self.cavity2L[0] - self.cavityradius - config.dfIDTpadPitch/2.0
        padLy = self.cavity2L[1]
        padL = gdspy.Rectangle((padLx - config.dfBiaspadSize/2, padLy - config.dfBiaspadSize/2.0),
                               (padLx + config.dfBiaspadSize/2, padLy + config.dfBiaspadSize/2.0), layer=self.metallayer)

        #right pad
        padRx = self.cavity2L[0] - self.cavityradius + config.dfIDTpadPitch / 2.0
        padRy = self.cavity2L[1]
        padR = gdspy.Rectangle((padRx - config.dfBiaspadSize / 2, padRy - config.dfBiaspadSize / 2.0),
                               (padRx + config.dfBiaspadSize / 2, padRy + config.dfBiaspadSize / 2.0), layer=self.metallayer)

        #linkpadth
        linkpathup = [ (xup, yup), (xup, yup + 50.0), (padLx, yup+50.0), (padLx, padLy + config.dfBiaspadSize/2.0)]
        linkpathdown = [(xdown, ydown), (xdown, padRy), (padRx  + config.dfBiaspadSize / 2.0, padRy)]
        linkL = gdspy.PolyPath(linkpathup, width=config.dfBiasLongWiring, layer=self.metallayer)
        linkR = gdspy.PolyPath(linkpathdown, width=config.dfBiasLongWiring, layer=self.metallayer)

        merged = gdspy.fast_boolean([padL, padR, upperelectrode, lowerelectrode, linkL, linkR], None, "or", layer = self.metallayer)
        self.add(merged)
        pass

    def createSuspendingOpening(self):
        self.protected = []
        # create openings for SAW part
        xmid = (self.cavity2L[0] + self.cavity2R[0]) / 2.0
        x0 = xmid - self.slabLength / 2.0 - 2.0 * config.dfOpeningWidth - config.dfOpeningConnection
        y0 = self.cavity2L[1] - self.cavityradius
        x1 = xmid + self.slabLength / 2.0 + 2.0 * config.dfOpeningWidth + config.dfOpeningConnection
        y1 = self.cavity2R[1] - self.cavityradius

        zone = gdspy.Rectangle((x0, y0 + 3*config.dfOpeningOffset), (x1, y1 - 3.0*config.dfOpeningOffset), layer = 0)
        self.protected.append(zone)

        # top opening
        topopen = gdspy.Rectangle((x0 + config.dfOpeningConnection, y0 + config.dfOpeningOffset),
                                  (x1 - config.dfOpeningConnection, y0 + config.dfOpeningOffset + 1.5 * config.dfOpeningWidth),
                                  layer=self.suslayer)

        # bottom opening
        bottomopen = gdspy.Rectangle((x0, y0 + config.dfOpeningOffset - self.slabWidth),
                                     (x1, y0 + config.dfOpeningOffset - self.slabWidth - 1.5 * config.dfOpeningWidth),
                                     layer=self.suslayer)

        # left opening
        leftopen = gdspy.Rectangle((x0 + 0.5*config.dfOpeningConnection, y0 - config.dfOpeningOffset ),
                                   (x0 + config.dfOpeningConnection + 2.0 * config.dfOpeningWidth,
                                    y0 + config.dfOpeningOffset - self.slabWidth + 3.5 * config.dfIDTpitch),
                                   layer=self.suslayer)

        # right opening
        rightopen = gdspy.Rectangle((x1 - 0.5*config.dfOpeningConnection, y1 - config.dfOpeningOffset ),
                                    (x1 - config.dfOpeningConnection - 2.0 * config.dfOpeningWidth,
                                     y1 + config.dfOpeningOffset - self.slabWidth + 3.5 * config.dfIDTpitch),
                                    layer=self.suslayer)

        self.add([topopen, bottomopen, leftopen, rightopen])


        #create openting for Bias electrodes
        xmid = (self.cavity2L[0] + self.cavity2R[0]) / 2.0
        x0 = self.cavity2L[0]
        y0 = self.cavity2L[1] + self.cavityradius
        x1 = self.cavity2R[0]
        y1 = self.cavity2R[1] + self.cavityradius
        #for openings
        topleft = gdspy.Rectangle( (x0, y0 + config.dfBiasLongWiring + self.IDToffset + config.dfOpeningOffset/2.0),
                                   (xmid - config.dfBiasLongWiring/2.0 - config.dfOpeningOffset/2.0 , y1 + config.dfBiasLongWiring + self.IDToffset + 2*config.dfOpeningWidth),
                                   layer = self.suslayer)
        topright = gdspy.Rectangle( (x1, y1 + config.dfBiasLongWiring + self.IDToffset + config.dfOpeningOffset/2.0),
                                   (xmid + config.dfBiasLongWiring/2.0 + config.dfOpeningOffset/2.0 , y1 + config.dfBiasLongWiring + self.IDToffset + 2*config.dfOpeningWidth),
                                   layer = self.suslayer)
        btmleft = gdspy.Rectangle( (x0, y0 - config.dfBiasLongWiring - self.IDToffset - config.dfOpeningOffset/2.0),
                                   (xmid - config.dfBiasLongWiring/2.0 - config.dfOpeningOffset/2.0 , y1 - config.dfBiasLongWiring - self.IDToffset - 2*config.dfOpeningWidth),
                                   layer = self.suslayer)
        btmright = gdspy.Rectangle( (x1, y1 - config.dfBiasLongWiring - self.IDToffset - config.dfOpeningOffset/2.0),
                                   (xmid + config.dfBiasLongWiring/2.0 + config.dfOpeningOffset/2.0 , y1 - config.dfBiasLongWiring - self.IDToffset - 2*config.dfOpeningWidth),
                                   layer = self.suslayer)


        zone = gdspy.Rectangle((x0 - 0.5*config.dfOpeningConnection , y0 + 3 * config.dfOpeningOffset), (x1 + 0.5*config.dfOpeningConnection, y1 - 3.0 * config.dfOpeningOffset), layer=0)
        self.protected.append(zone)

        self.add([topleft, topright, btmleft, btmright])


        ## add opening for regular path
        #openwg1 = _createsuspath(self.path_wg1, self.suslayer)
        openwg2 = _createsuspath(self.path_wg2, self.suslayer)
        #opencavity1 = _createsuspath(self.path_cavity1, self.suslayer)
        opencavity2 = _createsuspath(self.path_cavity2, self.suslayer)

        #fatwg1 = gdspy.PolyPath(self.path_wg1, width=2*config.dfOpeningOffset, max_points=199, layer=0, corners=1)
        fatwg2 = gdspy.PolyPath(self.path_wg2, width=2 * config.dfOpeningOffset, max_points=199, layer=0, corners=1)
        #fatcavity1 = gdspy.PolyPath(self.path_cavity1, width=2 * config.dfOpeningOffset, max_points=199, layer=0, corners=1)
        fatcavity2 = gdspy.PolyPath(self.path_cavity2, width=2 * config.dfOpeningOffset, max_points=199, layer=0, corners=1)

        #self.protected.extend([fatwg1, fatwg2, fatcavity1, fatcavity2])
        self.protected.extend([fatwg2, fatcavity2])

        fatwgTot = gdspy.fast_boolean(self.protected, None, "or", precision= 0.05)
        #openwg1 = gdspy.fast_boolean(openwg1, fatwgTot, "not", precision = 0.05, layer=self.suslayer)
        openwg2 = gdspy.fast_boolean(openwg2, fatwgTot, "not", precision=0.05, layer=self.suslayer)
        #opencavity1 = gdspy.fast_boolean(opencavity1, fatwgTot, "not", precision = 0.05, layer=self.suslayer)
        opencavity2 = gdspy.fast_boolean(opencavity2, fatwgTot, "not", precision=0.05, layer=self.suslayer)


        #self.add([openwg1, openwg2, opencavity1, opencavity2])
        self.add([openwg2, opencavity2])

        pass





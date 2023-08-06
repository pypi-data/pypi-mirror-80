from gdspy import Cell
import gdspy
import numpy as np
import warnings

from . import config


class IDTcell(Cell):
    """
    IDT cell
    """
    width = 100.0
    fingerwidth = 1.0
    fingerpitch = 0.5
    n = 20
    metallayer = 30
    direction = 1
    padlayer = -1
    extraconnect = config.dfIDTpadSize

    def __init__(self, name, width, fingerwidth, fingerpitch, n, direction=1, extraconnect = config.dfIDTpadSize ,metallayer = 30, *, padlayer = -1):
        Cell.__init__(self, name = name)
        self.width = width
        self.fingerwidth = fingerwidth
        self.fingerpitch = fingerpitch
        self.n = n
        self.metallayer = metallayer
        self.direction = direction
        self.extraconnect = extraconnect
        self.padlayer = padlayer

        self.createMask()
        pass


    def createMask(self):
        cellref = _metalIDTFingers(self.name,
                                   width = self.width,
                                   fingerwidth= self.fingerwidth,
                                   pitch = self.fingerpitch,
                                   n = self.n,
                                   connectwidth = config.dfIDTLongWiring,
                                   connectionLength= self.n * self.fingerpitch + self.extraconnect*0.5,
                                   metallayer= self.metallayer,
                                   padsFlag= True,
                                   padlayer = self.padlayer
                                   )

        if self.direction == 1:
            self.add( gdspy.CellReference(cellref, rotation=180.0 ))
        else:
            self.add(gdspy.CellReference(cellref, rotation=0.0))

        return None



class SPUDTcell(Cell):
    """
    SPUDT cell
    """
    width = 100.0
    fingerwidth = 1.0
    fingerpitch = 0.5
    n = 20
    metallayer = 30
    direction = 1
    padlayer = -1
    extraconnect = config.dfIDTpadSize

    def __init__(self, name, width, fingerpitch, n, direction=1, extraconnect = config.dfIDTpadSize ,metallayer = 30, *, padlayer = -1):
        Cell.__init__(self, name = name+str(config._index()))
        self.width = width
        self.fingerwidth = fingerpitch/2.0
        self.fingerpitch = fingerpitch
        self.n = n
        self.metallayer = metallayer
        self.direction = direction
        self.extraconnect = extraconnect
        self.padlayer = padlayer

        self.createMask()
        pass


    def createMask(self):
        cellref = _metalSPUDTFingers(self.name,
                                  width = self.width,
                                   pitch = self.fingerpitch,
                                   n = self.n,
                                   connectwidth = config.dfIDTLongWiring,
                                   connectionLength= 2.0*self.n * self.fingerpitch + self.extraconnect*0.5,
                                   metallayer= self.metallayer,
                                   padsFlag= True,
                                   padlayer = self.padlayer
                                   )

        if self.direction == 1:
            self.add( gdspy.CellReference(cellref, rotation=180.0 ))
        else:
            self.add(gdspy.CellReference(cellref, rotation=0.0))

        return None




def _metalIDTFingers(name, width, fingerwidth, pitch, n, connectwidth, connectionLength, metallayer = 30, fingerStart = -1, padsFlag = False, *, padlayer = -1):
    """
    generate IDT fingers width side connections
    :param name:
    :param width:
    :param fingerwidth:
    :param pitch:
    :param n:
    :param connectwidth:
    :param metallayer:
    :return: gdspy.Cell -- IDT fingers, with the (0, 0) at the edge of first metal finger.
    """
    cell0 = gdspy.Cell(name + "_%d"%config._index())

    positions = [pitch * i for i in range(0, n)]
    ## build IDT fingers ##
    gnd = fingerStart
    for position in positions:
        shiftx = gnd * pitch/2.0
        rectangle = gdspy.Rectangle((- shiftx - width / 2.0, position),
                                    (- shiftx + width / 2, position + fingerwidth), layer=metallayer)
        cell0.add(rectangle)
        gnd = gnd * -1

    ### Draw connection  ##
    rectangle = gdspy.Rectangle((-pitch/2.0 - width / 2.0 - connectwidth, 0.0 ),
                                (-pitch/2.0 - width / 2.0, connectionLength), layer=metallayer)
    cell0.add(rectangle)

    rectangle = gdspy.Rectangle((+pitch/2.0 + width / 2.0, 0.0 ),
                                (+pitch/2.0 + width / 2.0 + connectwidth, connectionLength), layer=metallayer)
    cell0.add(rectangle)


    #######  Draw  pads ###########
    if padsFlag:
        ############## Extra connection for small IDTs #########
        if width < config.dfIDTpadPitch - config.dfIDTpadSize:
            rectangle = gdspy.Rectangle( (- width / 2.0 -pitch/2.0, connectionLength),
                                         ( - 0.5*(-config.dfIDTpadSize + config.dfIDTpadPitch) , connectionLength + config.dfIDTLongWiring),
                                         layer=metallayer)

            cell0.add(rectangle)

            rectangle = gdspy.Rectangle( (width / 2.0 + pitch/2.0, connectionLength),
                                         ( 0.5*(-config.dfIDTpadSize + config.dfIDTpadPitch) , connectionLength + config.dfIDTLongWiring),
                                         layer=metallayer)

            cell0.add(rectangle)

        ############## Extra connnection for large pad ##########
        if width+pitch + 2.0*connectwidth > config.dfIDTpadSize + config.dfIDTpadPitch:
            rectangle = gdspy.Rectangle( (-pitch/2.0 - width / 2.0 - connectwidth, connectionLength),
                                         ( - 0.5*(config.dfIDTpadSize + config.dfIDTpadPitch) , connectionLength + config.dfIDTLongWiring),
                                         layer=metallayer)

            cell0.add(rectangle)

            rectangle = gdspy.Rectangle( (pitch/2.0 + width / 2.0 + connectwidth, connectionLength),
                                         ( 0.5*(config.dfIDTpadSize + config.dfIDTpadPitch) , connectionLength + config.dfIDTLongWiring),
                                         layer=metallayer)

            cell0.add(rectangle)

        #################  Draw Pads ############################
        ##pad layer
        if padlayer == -1:
            padlayer = metallayer
            overlap = 0.0
        else:
            overlap = 5.0
        ## assuming pitch = 150 um #############
        rectangle = gdspy.Rectangle((-config.dfIDTpadPitch / 2.0 - config.dfIDTpadSize / 2.0, connectionLength - overlap ),
                                    (-config.dfIDTpadPitch / 2.0 + config.dfIDTpadSize / 2.0, connectionLength + config.dfIDTpadSize), layer=padlayer)
        cell0.add(rectangle)

        rectangle = gdspy.Rectangle((+config.dfIDTpadPitch / 2.0 - config.dfIDTpadSize / 2.0, connectionLength - overlap),
                                    (+config.dfIDTpadPitch / 2.0 + config.dfIDTpadSize / 2.0, connectionLength + config.dfIDTpadSize), layer=padlayer)

        cell0.add(rectangle)

        pass

    #return
    return cell0



def _metalSPUDTFingers(name, width, pitch, n, connectwidth, connectionLength, metallayer = 30, fingerStart = -1, padsFlag = False, *, padlayer = -1):
    """
    generate SPUDT fingers width side connections
    REFERENCE:
    S. Lehtonen, V. P. Plessky, C. S. Hartmann, and M. M. Salomaa,
    "Unidirectional SAW transducer for gigahertz frequencies,"
    IEEE Transactions on Ultrasonics, Ferroelectrics, and Frequency Control 50, 1404-1406 (2003).

    :param name:
    :param width:
    :param pitch:
    :param n:
    :param connectwidth:
    :param metallayer:
    :return: gdspy.Cell -- IDT fingers, with the (0, 0) at the edge of first metal finger.
    """
    cell0 = gdspy.Cell(name + "_%d"%config._index())

    fingerwidth = pitch/2.0
    N1 = n//2
    if ( n % 2):
        print(f"[WARNING optohedge], SPUDT number of electrodes not in 2X. using number of electrodes 2*N1={2*N1} instead of n={n}")

    ## build IDT fingers ##
    position = 0

    gnd = fingerStart
    for i in range(0,N1):
        #electrode 1
        shiftx = gnd * pitch/2.0
        rectangle = gdspy.Rectangle((- shiftx - width / 2.0, position),
                                    (- shiftx + width / 2.0, position + fingerwidth), layer=metallayer)
        cell0.add(rectangle)
        gnd = gnd * -1

        # electrode 2
        position += pitch
        shiftx = gnd * pitch / 2.0
        rectangle = gdspy.Rectangle((- shiftx - width / 2.0, position),
                                    (- shiftx + width / 2.0, position + fingerwidth), layer=metallayer)
        cell0.add(rectangle)
        gnd = gnd * -1

        #reflector
        position += pitch
        rectangle = gdspy.Rectangle(( +pitch/2.0 - width / 2.0, position),
                                    ( -pitch/2.0 + width / 2.0, position + pitch), layer=metallayer)
        cell0.add(rectangle)
        position += 2.0 * pitch

    ### Draw connection  ##
    rectangle = gdspy.Rectangle((-pitch/2.0 - width / 2.0 - connectwidth, 0.0 ),
                                (-pitch/2.0 - width / 2.0, connectionLength), layer=metallayer)
    cell0.add(rectangle)

    rectangle = gdspy.Rectangle((+pitch/2.0 + width / 2.0, 0.0 ),
                                (+pitch/2.0 + width / 2.0 + connectwidth, connectionLength), layer=metallayer)
    cell0.add(rectangle)


    #######  Draw  pads ###########
    if padsFlag:
        ############## Extra connection for small IDTs #########
        if width < config.dfIDTpadPitch - config.dfIDTpadSize:
            rectangle = gdspy.Rectangle( (- width / 2.0 -pitch/2.0, connectionLength),
                                         ( - 0.5*(-config.dfIDTpadSize + config.dfIDTpadPitch) , connectionLength + config.dfIDTLongWiring),
                                         layer=metallayer)

            cell0.add(rectangle)

            rectangle = gdspy.Rectangle( (width / 2.0 + pitch/2.0, connectionLength),
                                         ( 0.5*(-config.dfIDTpadSize + config.dfIDTpadPitch) , connectionLength + config.dfIDTLongWiring),
                                         layer=metallayer)

            cell0.add(rectangle)

        ############## Extra connnection for large pad ##########
        if width+pitch + 2.0*connectwidth > config.dfIDTpadSize + config.dfIDTpadPitch:
            rectangle = gdspy.Rectangle( (-pitch/2.0 - width / 2.0 - connectwidth, connectionLength),
                                         ( - 0.5*(config.dfIDTpadSize + config.dfIDTpadPitch) , connectionLength + config.dfIDTLongWiring),
                                         layer=metallayer)

            cell0.add(rectangle)

            rectangle = gdspy.Rectangle( (pitch/2.0 + width / 2.0 + connectwidth, connectionLength),
                                         ( 0.5*(config.dfIDTpadSize + config.dfIDTpadPitch) , connectionLength + config.dfIDTLongWiring),
                                         layer=metallayer)

            cell0.add(rectangle)

        #################  Draw Pads ############################
        ##pad layer
        if padlayer == -1:
            padlayer = metallayer
            overlap = 0.0
        else:
            overlap = 10.0
        ## assuming pitch = 150 um #############
        rectangle = gdspy.Rectangle((-config.dfIDTpadPitch / 2.0 - config.dfIDTpadSize / 2.0, connectionLength - overlap ),
                                    (-config.dfIDTpadPitch / 2.0 + config.dfIDTpadSize / 2.0, connectionLength + config.dfIDTpadSize), layer=padlayer)
        cell0.add(rectangle)

        rectangle = gdspy.Rectangle((+config.dfIDTpadPitch / 2.0 - config.dfIDTpadSize / 2.0, connectionLength - overlap),
                                    (+config.dfIDTpadPitch / 2.0 + config.dfIDTpadSize / 2.0, connectionLength + config.dfIDTpadSize), layer=padlayer)

        cell0.add(rectangle)

        pass

    #return
    return cell0




#########################################################
#   IDT part -- generation  -- at center                #
#########################################################
def _metalSideIDTgen(widthx = 150.0, widthy = 2.0/2.0, pitch = 2.0, n=10, shift = 5.0, cellname="metalsideIDT", layer = 1, padlayer=3):
    global index
    index = index + 1
    cell0 = gdspy.Cell(cellname + "_gen%d" % (index))

    positions = [pitch*i for i in range(0, n)]
################ build connections #############
    gnd = -1
    for position in positions:
        shiftx = gnd * shift
        rectangle = gdspy.Rectangle((- shiftx - widthx / 2.0, position - widthy / 2.0),
                                     (- shiftx + widthx / 2, position + widthy / 2), layer=layer)
        cell0.add(rectangle)
        gnd = gnd * -1

############### Draw connection  ######
    rectangle = gdspy.Rectangle((-shift - widthx / 2.0 - 10.0, pitch - widthy / 2.0),
                                (-shift - widthx / 2.0 , max(pitch*(n-1)+widthy/2.0, 150.0) ), layer=layer)
    cell0.add(rectangle)

    rectangle = gdspy.Rectangle((+shift + widthx / 2.0 , - widthy / 2.0),
                                (+shift + widthx / 2.0 + 10.0 ,  pitch*(n-2)+widthy/2.0 ), layer=layer)
    cell0.add(rectangle)


    rectangle = gdspy.Rectangle((-shift - widthx / 2.0 - 80.0, 130.0),
                                (-shift - widthx / 2.0 - 10.0, 150.0), layer=layer)
    cell0.add(rectangle)

    rectangle = gdspy.Rectangle((-shift - widthx / 2.0 - 80.0, + widthy / 2.0),
                                (shift - widthx / 2.0, min(- widthy / 2.0, + widthy / 2.0 - 20.0)), layer=layer)
    cell0.add(rectangle)

############### Draw Pads  ######
    ### Assumeing 150 um pitch
    rectangle = gdspy.Rectangle((-shift - widthx / 2.0 - 80.0 -120.0 , -120.0/2.0),
                                (-shift - widthx / 2.0 - 80.0, 120.0/2 ), layer=padlayer)
    cell0.add(rectangle)

    rectangle = gdspy.Rectangle((-shift - widthx / 2.0 - 80.0 -120.0 , 150.0-120.0/2.0),
                                (-shift - widthx / 2.0 - 80.0, 150.0+120.0/2 ), layer=padlayer)
    cell0.add(rectangle)

    print("metalIDT at center generated.")
    return cell0


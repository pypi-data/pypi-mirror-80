############################################################
# This file contains the module-wise tag configurations
###########################################################


# output more infomation?
INFO = True

# global setting and variables for optical cells


#GDSII setting
MAXPOINTS = 8190


# _index --  do not change, this is just a globle index to avoid naming conflicts of Cell
__index = 1  # never directly change this


def _index():
    global __index
    __index += 1
    return __index

#pathnodes
dfpathnodesResolution = 0.1

# optical Cell
dfoptwgwidth = 0.85
dfTurningRadius = 95.0
dfFieldGuideLayer = 0
dfFieldSize = 500.0
dfOptRes = 0.3

# Suspended optical class settings
dfOpeningLength = 20.0
dfOpeningWidth = 1.2
dfOpeningConnection = 2.0
dfOpeningOffset = 2.0
dfSkipPathNodes = 2    # reduce the number of points for the suspending region, to reduce file sizes

# SAW metal settings
dfIDTpitch = 1.0
dfIDTwidth = 0.5
dfIDTpadSize = 75.0
dfIDTpadPitch = 150.0
dfIDTLongWiring = 10.0
dfBiaspadSize = 50.0
dfBiasLongWiring = 4.0

#acousto 0 optics
dfAlignmentOverLay = 0.1

#Positive Resist Optical Cells
dfPosOptCellOpening = 5.0


#acoustic Cells
dfAcuwgWidth = 5.0
dfAcuwgExtend = 30.0
dfAcuRes = 0.1


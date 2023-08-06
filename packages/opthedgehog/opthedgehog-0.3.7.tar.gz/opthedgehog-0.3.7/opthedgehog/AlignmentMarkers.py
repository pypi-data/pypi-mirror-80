import gdspy

from .config import _index


######################################################################
# add allignment Marker                                              #
# Standard Alignment Marker for both Ebeam and photolithography      #
######################################################################


def alignmentMarker(cellname="alignmentmarker", layer=10, layerOPEN=50, *, finefeature = 3. ):
    """
    Alignment Marker for both photolithography and ebeam lithography.

    The default is tested good for both EL-5 and OL-10

    Args:
        cellname: str
        layer: int, default *10* -- layer for the marker pattern.
        layerOPEN: int, default *50* -- layer for exposure of the alignment marker region, it's a large square covering the marker.
        finefeature: float, default *3.0* --  the size of the alignment feature, in unit of um.

    Returns:
        gdspy.Cell

    """
    cell1 = gdspy.Cell(cellname + "_" + str(_index()))
    # cell1.add(gdspy.Polygon([(0, 100), (-50, 250), (50, 250)], layer = layer))  # UP
    cell1.add(gdspy.Polygon([(0, -100), (-30, -150), (30, -150)], layer=layer))  # Down
    # cell1.add(gdspy.Polygon([(100, 0), (250, 50), (250, -50)], layer = layer))  # right
    cell1.add(gdspy.Polygon([(-100, 0), (-150, 30), (-150, -30)], layer=layer))  # left

    cell1.add(gdspy.Rectangle((-100, -finefeature), (-finefeature*5/3., finefeature), layer=layer))
    cell1.add(gdspy.Rectangle((100, -finefeature), (finefeature*5/3., finefeature), layer=layer))
    cell1.add(gdspy.Rectangle((-finefeature, 100), (finefeature, finefeature*5/3.), layer=layer))
    cell1.add(gdspy.Rectangle((-finefeature, -100), (finefeature, -finefeature*5/3.), layer=layer))

    cell1.add(gdspy.Rectangle((0, 0), (finefeature, finefeature), layer=layer))
    cell1.add(gdspy.Rectangle((0, 0), (-finefeature, -finefeature), layer=layer))

    # open window for ebeam alignment
    cell1.add(gdspy.Rectangle((-180, -180), (180, 180), layer=layerOPEN))

    return cell1


#########################################################
# add text                                              #
#########################################################
def textCell(text="Loncar Group", size=20, cellname="text", layer=10):
    cell1 = gdspy.Cell(cellname + str(_index()))

    text1 = gdspy.Text(text, size, (0, 0), layer=layer)
    label1 = gdspy.Label(text, (0, -5), 'nw', layer=layer)
    cell1.add(text1)
    cell1.add(label1)
    print("[OptHedgehog Info]     text cell added: " + text)
    return cell1


##########################################################
# alignment test cell
# added Dec 11, 2019
##########################################################
def alignCheckMarker(name = "alignChecker", layer1 = 10, layer2 = 20, *, resolution=0.5 ):
    """
    aligned pattern to check alignment only, not for alignment
    """
    cell1 = gdspy.Cell(name+str(_index()))

    #guide pattern lines
    cell1.add(gdspy.Polygon([(-40, 0), (-80, 30), (-80, -30)], layer=layer1))
    cell1.add(gdspy.Rectangle((-40, -2), (-8, 2), layer=layer1))
    cell1.add(gdspy.Rectangle((40, -2), (8, 2), layer=layer1))
    cell1.add(gdspy.Rectangle((-2, 40), (2, 8), layer=layer1))
    cell1.add(gdspy.Rectangle((-2, -40), (2, -8), layer=layer1))

    #label
    cell1.add(gdspy.Text(f"{layer1}=={layer2}\n{resolution}", 10, (20,35), layer=layer2) )

    #first layer pattern
    cell1.add(gdspy.Rectangle((-8.0, -resolution / 2.0), (8.0, resolution / 2.0), layer=layer1))
    cell1.add(gdspy.Rectangle((-resolution / 2.0, -8.0), (resolution / 2.0, 8.0), layer=layer1))

    cell1.add(gdspy.Rectangle((-1.5*resolution, 3.0*resolution / 2.0), (1.5*resolution, 5.0*resolution / 2.0), layer=layer1))

    #second layer
    cell1.add(gdspy.Rectangle((-7.0, 1.5 * resolution), (-1.5 * resolution, 7.0), layer=layer2))
    cell1.add(gdspy.Rectangle((-7.0, -1.5 * resolution), (-1.5 * resolution, -7.0), layer=layer2))
    cell1.add(gdspy.Rectangle((7.0, -1.5 * resolution), (1.5 * resolution, -7.0), layer=layer2))
    cell1.add(gdspy.Rectangle((7.0, 1.5 * resolution), (1.5 * resolution, 7.0), layer=layer2))

    return cell1
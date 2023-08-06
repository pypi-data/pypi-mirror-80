#
#  collection of electronic soldering footprint
#  Linbo Shao 2020
#


from gdspy import Cell
import gdspy
import numpy as np
import warnings

from .optCells import OptCell
from .config import _index
from . import config
from typing import List, Tuple




class SMT2pin(OptCell):
    """
    Footprint for SMT elements

    Args:
        name: str,
        inports: List[Tuple[float, float, float, float]], one of the pad postion
        sizetype: string, From inch based "0201", "0402", "0603", "0805"
        angle: float, in degree, the angle to the X axis
        layer: int, default *35*

    Global Parameters:

    Example:
        >>>
    """


    dimension = {
        "0201": {"A": 370, "B": 280, "C": 280},
        "0402": {"A": 535, "B": 410, "C": 405},
        "0603": {"A": 900, "B": 660, "C": 700},
        "0805": {"A": 1320, "B": 660, "C": 1090},
    }

    sizetype = ""
    angledeg = 0.

    def __init__(self,
                 name:str,
                 inports: List[Tuple[float, float, float, float]],
                 sizetype:str,
                 angle: float = 0,
                 layer: int = 35):
        super().__init__(name, layer)
        self.inports = inports
        self.sizetype = sizetype
        self.angledeg = angle

        self.createMask()
        pass

    def createMask(self):
        x0 ,y0, dx0, dy0 = self.inports[0]

        A = self.dimension[self.sizetype]["A"]
        B = self.dimension[self.sizetype]["B"]
        C = self.dimension[self.sizetype]["C"]

        cell1 = gdspy.Cell(self.name+str(_index()),exclude_from_current=True)

        #firstPad
        pad1 = gdspy.Rectangle((-B/2, -A/2), (B/2, A/2), layer=self.layer)
        pad2 = gdspy.Rectangle((C+B-B/2, -A/2), (C+B+B/2, A/2), layer=self.layer)
        cell1.add(pad1)
        cell1.add(pad2)

        self.add(gdspy.CellReference(cell1, (x0, y0), self.angledeg ))
        self.flatten()

        anglerad = self.angledeg / 180.0 * np.pi
        dx, dy = np.cos(anglerad), np.sin(anglerad)
        xend, yend = x0 + dx * (C+B), y0 + dy * (C+B)

        self.outports = [(xend, yend, dx0, dy0)]


        pass

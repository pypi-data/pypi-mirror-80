#
#  collection of helper functions
#  Linbo Shao 2020
#
__author__ = "Linbo shao"


import gdspy
from typing import Iterable, Union


def estimateWritingTimeReport(cell : gdspy.Cell, dose: Union[float, Iterable[float]] = 1200, current: Union[float, Iterable[float]] = 2, layers = None):
    """
        Estimate Ebeam writing time

        Args:
            cell: gdspy.Cell
            dose: float OR Iterable[float], default 1200,  dose of the resist in unit of  uC/cm^2
            current: float or Iterable[float],  current of the electron beam, in unit of nA
            layers: None or List[int], the layer number to be analyzed, None for all layers.

        Example:
            >>> estimateWritingTimeReport(ebeam, dose = [1500, 1200], current= 5, layers=[10, 20])

        """

    from datetime import timedelta
    try:
        it = iter(dose)
    except TypeError:
        dose = [dose]

    try:
        it = iter(current)
    except TypeError:
        current = [current]

    print("[opthedgehog]")
    print("---------------  Ebeam writing time analysis  --------------- ")
    areas = cell.area(by_spec=True)
    for spec in areas:
        area = areas[spec]
        layer, tmp = spec
        if layers == None or layer in layers:
            print(f" -- Layer  {layer} --- ")
            print(f" Area:  {area:.2f} um^2")
            for c in current:
                for d in dose:
                    time = area / 1e8 * d / c * 1e3 * 1.1923847
                    print(f"Dose {d} uC/cm^2   Current {c} nA    Estimated writing time {timedelta(seconds=time)}. ")

    print(" -------------  END of Ebeam writing time analysis ---------- ")
    print("[opthedgehog]")
import numpy as np
from Geometry2D.Basis2D import *
import Checker

class Circle():
    def __init__(self, center: Point2D | Tuple[int, int], radius: int):
        if not isinstance(center, Point2D):
            center = Point2D(*center)
        elif not isinstance(center, Tuple):
            raise ValueError("Point must be Tuple[int, int] or Point2D")
        self.__center = center
        self.__radius = radius

    @property
    def radius(self) -> int:
        return self.__radius
    
    @radius.setter
    def radius(self, new: int):
        Checker.check_radius(new)
        self.__radius = new

    @property
    def center(self) -> Point2D:
        return self.__center
    
    @center.setter
    def radius(self, new: Point2D | Tuple[int, int]):
        if not isinstance(new, Point2D):
            self.__center = Point2D(*new)
        elif not isinstance(new, Tuple):
            raise ValueError("Point must be Tuple[int, int] or Point2D")
        self.__radius = new

    def draw_circle(self) -> list[Point2D]:
        pass
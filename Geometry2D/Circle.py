import numpy as np
from Geometry2D.Basis2D import *
from Geometry2D.Polygon2D import Polygon2D
import Checker

class Circle(Polygon2D):
    def __init__(self, center: Point2D, radius: int, primary):
        self.center = center
        self.radius = radius

        
        points = []
        p = Point2D()
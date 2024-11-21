import numpy as np
from sympy import true
from Geometry2D.Basis2D import *
from Geometry2D.CoordinateSys2D import *
import Checker

class Polygon2D(CoordinateSys2D):
    def __init__(self, segments: list | list[Segment2D] | np.ndarray):
        points = []
        self.__segments = []
        for p1, p2 in segments:
            points.append(p1)
            points.append(p2)
            if isinstance(p1, Point2D):
                self.__segments.append(Segment2D(p1, p2))
            else:
                self.segments.append(Segment2D(Point2D(*p1), Point2D(*p2)))
        super().__init__(points)
        super().refine()
        
    @property
    def segments(self):
        return self.__segments

class ConvexHull2D(CoordinateSys2D):
    def __init__(self, points, primary: str = "x"):
        super().__init__(points, primary)
        super().sort_points()
        self.__points = self.__convert()
        self.__all_points = points
        del self.sort_points
        del self.is_points_sorted

    @property 
    def all_points(self):
        return self.__all_points

    def _convert(self) -> list:
        # Monotone chain algorithm
        st = [self.points[0], self.points[1]]
        
        # Upper hull
        for p in self.points[2::]:
            direction = Fundamental2D.direction(p, st[-1], st[-2])
            while direction >= 0 and len(st) >= 2:
                st.pop()
                if len(st) >= 2:
                    direction = Fundamental2D.direction(p, st[-1], st[-2])
            st.append(p)
        outer_points = st[:-1:]
        
        # Lower hull
        st = [self.points[-1], self.points[-2]]
        for p in self.points[:-2:][::-1]:
            direction = Fundamental2D.direction(p, st[-1], st[-2])
            while direction >= 0 and len(st) >= 2:
                st.pop()
                if len(st) >= 2:
                    direction = Fundamental2D.direction(p, st[-1], st[-2])
            st.append(p)
        outer_points += st[:-1:]
        
        return outer_points
    
    def draw_border(self) -> list:
        self.refine()
        graph = []
        for idx in range(len(self.points)-1):
            p1, p2 = Point2D(*self.points[idx]), Point2D(*self.points[idx+1])
            graph += Segment2D(p1, p2).connection()[:-1:] 
        return graph
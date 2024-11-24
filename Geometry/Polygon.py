import numpy as np
from Geometry.Basis import *
from Geometry.Basis import Tuple
from Geometry.CoordinateSys import *
import Checker

class Polygon(CoordinateSys):
    def __init__(self, segments: list | list[Segment] | np.ndarray):
        points = []
        self.__segments = []
        for p1, p2 in segments:
            points.append(p1)
            points.append(p2)
            if isinstance(p1, Point):
                self.__segments.append(Segment(p1, p2))
            else:
                self.segments.append(Segment(Point(*p1), Point(*p2)))
        super().__init__(points)
        super().refine()
        
    @property
    def segments(self):
        return self.__segments

class ConvexHull(CoordinateSys):
    def __init__(self, points: list[Tuple[float, float]] | list[Point] | np.ndarray, primary: str = "x"):
        super().__init__(points, primary)
        super().sort_points()
        self.__points = self.__convert()
        self.__all_points = points

    @property 
    def all_points(self):
        return self.__all_points

    @property
    def convex_points(self):
        return self.__points

    def sort_points(self, *args, **kwargs):
        raise AttributeError("Sorting points is not allowed in convex hull")

    def is_points_sorted(self) -> bool:
        return True

    def __convert(self) -> list:
        # Monotone chain algorithm
        st = [self.points[0], self.points[1]]
        
        # Upper hull
        for p in self.points[2::]:
            direction = Fundamental.direction(p, st[-1], st[-2])
            while direction >= 0 and len(st) >= 2:
                st.pop()
                if len(st) >= 2:
                    direction = Fundamental.direction(p, st[-1], st[-2])
            st.append(p)
        outer_points = st[:-1:]
        
        # Lower hull
        st = [self.points[-1], self.points[-2]]
        for p in self.points[:-2:][::-1]:
            direction = Fundamental.direction(p, st[-1], st[-2])
            while direction >= 0 and len(st) >= 2:
                st.pop()
                if len(st) >= 2:
                    direction = Fundamental.direction(p, st[-1], st[-2])
            st.append(p)
        outer_points += st[:-1:]
        
        return outer_points
    
    def draw_border(self, **kwargs) -> list[Point] | list[Segment]:
        return super().draw_polygon(dividing_line=-1, **kwargs)
import numpy as np
from Geometry.Basis import *
from functools import total_ordering
import Checker
from typing import Tuple, List

@total_ordering
class BaseShape:
    def __init__():
        pass
    
    def draw(self, min_step: float = 1) -> List[Point]:
        pass
    
    def is_on_edge(self, p: Point | Tuple[float, float]) -> bool:
        pass
    
    @property
    def area(self) -> float:
        return None

    def __eq__(self, other) -> float:
        return False

    def __lt__(self, other):
        return NotImplemented

class Circle(BaseShape):
    def __init__(self, center: Point | Tuple[float, float], radius: float):
        if not isinstance(center, Point):
            center = Point(*center)
        self.__center = center
        self.__radius = radius

    @property
    def radius(self) -> float:
        return self.__radius
    
    @radius.setter
    def radius(self, new: float):
        Checker.check_radius(new)
        self.__radius = new

    @property
    def center(self) -> Point:
        return self.__center
    
    @center.setter
    def center(self, new: Point):
        self.__center = new

    def draw(self, min_step: float = 1) -> List[Point]:
        Checker.check_step(min_step)
        x, y = self.center
        
        max_p = []
        max_p.append(Point(x, y + self.radius))
        max_p.append(Point(x + self.radius, y))
        max_p.append(Point(x, y - self.radius))
        max_p.append(Point(x - self.radius, y))

        path = [
            [[0, min_step], [0, -min_step]],
            [[0, -min_step], [0, -min_step]],
            [[0, -min_step], [0, min_step]],
            [[0, min_step], [0, min_step]],
        ]
        
        cir = []
        res = []

        for idx in range(4):
            cir = []
            cir.append(max_p[idx])
            p = cir[0]
            x, y = cir[0]
            while p != max_p[(idx+1)%4]:
                minn = Fundamental.MAX
                x, y= cir[-1]
                for dx in path[idx][0]:
                    for dy in path[idx][1]:
                        if (dx, dy) == (0, 0):
                            continue
                        p_tmp = Point(x+dx, y+dy)
                        dis = self.center.distance_to(p_tmp)
                        dis = abs(dis-self.radius)
                        if dis < minn:
                            minn = dis
                            p = p_tmp
                cir.append(p)
            cir.pop()
            res += cir
        return res
    
    def is_on_edge(self, p: Point | Tuple[float, float]) -> bool:
        if not isinstance(p, Point):
            p = Point(*p)
        dis = self.center.distance_to(p)
        return math.isclose(dis, self.radius)

    @property
    def area(self) -> float:
        return self.radius ** 2 * Fundamental.Pi

    @property
    def angles(self) -> List[float]:
        return []

    @property
    def points(self) -> List[Point]:
        return []

    def __eq__(self, other: "Circle") -> bool:
        return (
            math.isclose(self.radius, other.radius)
            and
            self.center == other.center
        )
    
    def __lt__(self, other) -> bool:
        return NotImplemented
    
class Triangle(BaseShape):
    def __init__(self, p1: Point | Tuple[float, float], p2: Point | Tuple[float, float], p3: Point | Tuple[float, float]):
        if not isinstance(p1, Point):
            p1 = Point(*p1)
        if not isinstance(p2, Point):
            p2 = Point(*p2)
        if not isinstance(p3, Point):
            p3 = Point(*p3)
        Checker.check_coincided_point(p1, p2)
        Checker.check_coincided_point(p2, p3)
        Checker.check_coincided_point(p1, p3)

        p1, p2, p3 = sorted([p1, p2, p3])
        self.__p1 = p1
        self.__p2 = p2
        self.__p3 = p3
        
        self.__edge12 = Segment(p1, p2)
        self.__edge23 = Segment(p2, p3)
        self.__edge13 = Segment(p1, p3)
        
    @property
    def p1(self) -> Point:
        return self.__p1
    
    @property
    def p2(self) -> Point:
        return self.__p2

    @property
    def p3(self) -> Point:
        return self.__p3

    @property
    def angle12_23(self) -> float:
        return self.__edge12.angle_with(self.__edge23, closest=False)

    @property
    def angle12_13(self) -> float:
        return self.__edge12.angle_with(self.__edge13, closest=False)
    
    @property
    def angle13_23(self) -> float:
        return self.__edge13.angle_with(self.__edge23, closest=False)

    @property
    def angles(self) -> List[float]:
        return [
            self.angle12_23,
            self.angle12_13,
            self.angle13_23
        ]

    @property
    def points(self) -> List[Point]:
        return [self.p1, self.p2, self.p3]

    def draw(self, min_step: float = 1) -> List[Point]:
        segment12 = self.__edge12.connection(min_step)
        segment23 = self.__edge23.connection(min_step)
        segment13 = self.__edge13.connection(min_step)
        
        return segment23

    def __iter__(self):
        return iter([self.p1, self.p2, self.p3])
import numpy as np
from Geometry.Basis import *
import Checker
from typing import Tuple

class Circle():
    def __init__(self, center: Point | Tuple[float, float], radius: float):
        if not isinstance(center, Point):
            center = Point(*center)
        self.__center = center
        self.__radius = radius

    @property
    def radius(self):
        return self.__radius
    
    @radius.setter
    def radius(self, new: float):
        Checker.check_radius(new)
        self.__radius = new

    @property
    def center(self):
        return self.__center
    
    @center.setter
    def center(self, new: Point):
        self.__center = new

    def draw_circle(self, min_step: float = 1) -> list[Point]:
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
                        dis = self.center.distance_to(Point(x+dx, y+dy))
                        dis = abs(dis-self.radius)
                        if dis < minn:
                            minn = dis
                            p = Point(x+dx, y+dy)
                cir.append(p)
            cir.pop()
            res += cir
        return res
    
    def is_on_circle(self, p: Point | Tuple[float, float]) -> bool:
        if not isinstance(p, Point):
            p = Point(*p)
        dis = self.center.distance_to(p)
        return math.isclose(dis, self.radius)
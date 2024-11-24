import numpy as np
from Geometry.Basis import *
import Checker

class Circle():
    def __init__(self, center: Point | Tuple[float, float], radius: float):
        if not isinstance(center, Point):
            center = Point(*center)
        elif not isinstance(center, Tuple):
            raise ValueError("Point's type must be Tuple[float, float] or Point")
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
    def center(self, new: Point | Tuple[float, float]):
        if not isinstance(new, Point):
            self.__center = Point(*new)
        elif not isinstance(new, Tuple):
            raise ValueError("Point's type must be Tuple[float, float] or Point")
        self.__center = new

    def draw_circle(self) -> list[Point]:
        x, y = self.center
        
        max_p = []
        max_p.append(Point(x, y + self.radius))
        max_p.append(Point(x + self.radius, y))
        max_p.append(Point(x, y - self.radius))
        max_p.append(Point(x - self.radius, y))

        path = [
            [[0, 1], [0, 1]],
            [[0, -1], [0, -1]],
            [[0, -1], [0, 1]],
            [[0, 1], [0, -1]],
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
                for dx in path[idx][0]:
                    for dy in path[idx][1]:
                        if (dx, dy) == (0, 0):
                            continue
                        dis = self.center.distance_to(Point(x+dx, y+dy))
                        dis = abs(dis-self.radius)
                        if dis < minn:
                            minn = dis
                            p = Point(x+dx, y+dy)
                if len(cir) > 200:
                    exit()
                # print(cir[-1])
                cir.append(p)
            cir.pop()
            res += cir
        return res
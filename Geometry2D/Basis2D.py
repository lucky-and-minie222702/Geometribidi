import numpy as np
from functools import total_ordering
import Checker
from typing import Tuple
import math

@total_ordering
class Point2D:
    def to_points(points, primary: str = "x", angle: int = 0) -> list:
        points = [Point2D(*p, primary, angle)for p in points]
        return points

    def __init__(self, x: float, y: float, primary: str = "x", angle: int = 0, og: Tuple[int, int] = (0, 0)):
        self.__x = x
        self.__y = y
        Checker.check_primary_point(primary)
        Checker.check_angle(angle)
        self.__primary = primary
        self.__angle = angle
        self.__og = og
        
    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y
    
    @property
    def xy(self):
        return self.__x, self.__y
    
    @property 
    def primary(self):
        return self.__primary
    
    @property 
    def angle(self):
        return self.__angle

    def set_primary(self, primary: str):
        Checker.check_primary_point(primary)
        self.__primary = primary

    def rotate(self, angle: int, in_place: bool = True, return_new: bool = False):
        Checker.check_angle(angle)
        Checker.check_angle_for_rotate(angle)
        if in_place:
            self.__angle = angle
            angle = math.radians(angle)
            self.__x = self.x / math.sin(angle)
            self.__y = self.y / math.cos(angle)
        if return_new:
            angle = math.radians(angle)
            return Point2D(self.x / math.sin(angle), self.y / math.cos(angle))

    def set_og(self, x: float, y: float):
        self.__og = (x, y)

    def distance_to(self, other) -> float:
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2
        )
    
    def raw_coordinate(self):
        return self.x, self.y
    
    def shift_x(self, val: int, in_place: bool = True, return_new: bool = False):
        if in_place:
            self.__x += val
        if return_new:
            return Point2D(self.x + val, self.y)
    
    def shift_y(self, val: int, in_place: bool = True, return_new: bool = False):
        if in_place:
            self.__y += val
        if return_new:
            return Point2D(self.x + val, self.y)
    
    def __eq__(self, other) -> bool:
        if self.primary != "angle1" and not self.primary == "angle2":
            return self.x == other.x and self.y == other.y
        elif self.primary == "angle1":
            line1: Line2D = Line2D.from_fix_points(Point2D(*self.__og), self)
            line2: Line2D = Line2D.from_fix_points(Point2D(*self.__og), other)
            line3: Line2D = Line2D(0, 1, 0)
            ang1 = line1.angle_with(line3)
            ang2 = line2.angle_with(line3)
            return ang1 == ang2
        else:
            return Fundamental2D.direction(Point2D(*self.__og), self, other) == 0

    def __lt__(self, other) -> bool:
        if self.primary == "x":
            if self.x != other.x:
                return self.x < other.x
            else:
                return self.y < other.y
        elif self.primary == "y":
            if self.y != other.y:
                return self.y < other.y
            else:
                return self.x < other.x
        elif self.primary == "x_flip":
            if self.x != other.x:
                return self.x < other.x
            else:
                return self.y > other.y
        elif self.primary == "y_flip":
            if self.y != other.y:
                return self.y < other.y
            else:
                return self.x > other.x
        elif self.primary == "angle1":
            line1: Line2D = Line2D.from_fix_points(Point2D(*self.__og), self)
            line2: Line2D = Line2D.from_fix_points(Point2D(*self.__og), other)
            line3: Line2D = Line2D(0, 1, 0)
            ang1 = line1.angle_with(line3)
            ang2 = line2.angle_with(line3)
            return ang1 < ang2
        elif self.primary == "angle2":
            return Fundamental2D.direction(Point2D(*self.__og), self, other) == -1

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __iter__(self):
        return iter([self.x, self.y])

class Fundamental2D:
    def direction(A: Point2D, B: Point2D, C: Point2D) -> int:
        kq = (B.x - A.x) * (B.y + A.y) + (C.x - B.x) * (C.y + B.y) + (A.x - C.x) * (A.y + C.y)
        if kq < 0:
            return -1
        elif kq > 0:
            return 1
        else:
            return 0

class Line2D:
    def __init__(self, a: int, b: int, c: int):
        self.__coef_a = a
        self.__coef_b = b
        self.__coef_c = c
    @property
    def coef_a(self):
        return self.__coef_a

    @property
    def coef_b(self):
        return self.__coef_b
    
    @property
    def coef_c(self):
        return self.__coef_c
    
    @property
    def coefs(self):
        return self.coef_a, self.coef_b, self.coef_c

    def intersect(self, other):
        a1, b1, c1 = self.coef_a, self.coef_b, self.coef_c
        a2, b2, c2 = other.coef_a, other.coef_b, other.coef_c
        delta = a1 * b2 - a2 * b1

        if delta == 0:
            if a1 * c2 == a2 * c1 and b1 * c2 == b2 * c1:
                # coincident
                return 0
            else:
                # parallel
                return 0
        
        delta_x = -c1 * b2 + c2 * b1
        delta_y = -a1 * c2 + a2 * c1

        x = delta_x / delta
        y = delta_y / delta

        return x, y
            
    def from_slop_intercept(m: int, intercept: int, is_raw: bool = False):
        a = m
        b = -1
        c = -intercept
        if is_raw:
            return a, b, c
        else:
            return Line2D(a, b, c)
    
    def from_fix_points(p1: Point2D | Tuple[int, int], p2: Point2D | Tuple[int, int], is_raw: bool = False):
        if not isinstance(p1, Point2D):
            p1 = Point2D(*p1)
        if not isinstance(p2, Point2D):
            p2 = Point2D(*p2)
        a =  p2.y - p1.y
        b = p1.x - p2.x
        c = (p2.x * p1.y) - (p1.x * p2.y)
        if is_raw:
            return a, b, c
        else:
            return Line2D(a, b, c)

    def to_slope_intercept(self) -> Tuple[int, int]:
        a, b, c = self.coef_a, self.coef_b, self.coef_c
        if b != 0:
            m = -a / b
            intercept = -c / b
        else: 
            return None, None
        return m, intercept

    def distance_to(self, p: Point2D) -> float:
        a, b, c = self.coef_a, self.coef_b, self.coef_c
        top = abs(a * p.x + b * p.y + c) 
        bot = math.sqrt(a**2 + b**2)
        d = top / bot
        return d
    
    def angle_with(self, other, closest: bool = False):
        a1, b1, c1 = self.coef_a, self.coef_b, self.coef_c
        a2, b2, c2 = other.coef_a, other.coef_b, other.coef_c

        dot_product = a1 * a2 + b1 * b2
        magnitude1 = math.sqrt(a1**2 + b1**2)
        magnitude2 = math.sqrt(a2**2 + b2**2)
        
        if magnitude1 == 0 or magnitude2 == 0:
            # a == 0
            return None
        if closest:
            dot_product = abs(dot_product)
        cos_theta = dot_product / (magnitude1 * magnitude2)
        cos_theta = min(1, max(-1, cos_theta))
        
        theta = math.acos(cos_theta)
        theta_degrees = math.degrees(theta)
        
        return theta_degrees
    
    def x_to_y(self, x: int) -> float:
        y = -(self.coef_c + self.coef_a * x) / self.coef_b
        return y
    
    def x_y_range(self, start: int, count: int) -> list:
        x = start
        res = []
        while len(res) < count:
            if -(self.coef_c + self.coef_a * x) % self.coef_b == 0:
                res.append([x, self.x_to_y(x)])
            x += 1
        return res
        
    def __repr__(self) -> str:
        return f"{self.coef_a}x + {self.coef_a}y + {self.coef_c} = 0"

    def __iter__(self):
        return iter([self.coef_a, self.coef_b, self.coef_c])

class Segment2D(Line2D):
    def __init__(self, p1: Point2D, p2: Point2D, sort: bool = True):
        Checker.check_overlap_point(p1, p2)
        if p1 > p2 and sort:
            p1, p2 = p2, p1
        self.__p1 = p1 # small
        self.__p2 = p2 # large
        a, b, c = Line2D.from_fix_points(p1, p2, True)
        super().__init__(a, b, c)

    @property
    def p1(self):
        return self.__p1

    @property
    def p2(self):
        return self.__p2
    
    @property
    def xy(self):
        return self.p1.xy, self.p2.xy
    
    def length(self) -> float:
        return self.p1.distance_to(self.p2)

    def connection(self) -> list[Point2D]:
        last = (self.p1, self.p2)
        if self.p1 > self.p2:
            self.__p1, self.__p2 = self.p2, self.p1
        Line2D = []
        movex = [0, 1]
        movey = [0, 1] if self.p1.y < self.p2.y else [-1, 0]
        p = self.p1
        Line2D.append(p)
        while p != self.p2:
            x, y = Line2D[-1].x, Line2D[-1].y
            minn1, minn2 = 1e9, 1e9
            for dx in movex:
                for dy in movey:
                    if (dx, dy) == (0, 0):
                        continue
                    dis1 = self.distance_to(Point2D(x+dx, y+dy))
                    dis2 = self.p2.distance_to(Point2D(x+dx, y+dy))
                    if (dis1 <= minn1 and dis2 < minn2) or (dis1 < minn1 and dis2 <= minn2):
                        minn1 = dis1
                        minn2 = dis2
                        p = Point2D(x+dx, y+dy)
            Line2D.append(p)
        self.__p1, self.__p2 = last
        return Line2D
    
    def __repr__(self) -> str:
        return f"{self.p1} - {self.p2}"
    
    def __iter__(self):
        return iter([self.p1, self.p2])

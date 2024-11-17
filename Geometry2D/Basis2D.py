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
        self._x = x
        self._y = y
        Checker.check_primary_point(primary)
        Checker.check_angle(angle)
        self._primary = primary
        self._angle = angle
        self._og = og
        
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
    
    @property
    def xy(self):
        return self._x, self._y
    
    @property 
    def primary(self):
        return self._primary
    
    @property 
    def angle(self):
        return self._angle

    def set_primary(self, primary: str):
        Checker.check_primary_point(primary)
        self._primary = primary

    def rotate(self, angle: int, in_place: bool = True, return_new: bool = False):
        Checker.check_angle(angle)
        Checker.check_angle_for_rotate(angle)
        if in_place:
            self._angle = angle
            angle = math.radians(angle)
            self._x = self.x / math.sin(angle)
            self._y = self.y / math.cos(angle)
        if return_new:
            angle = math.radians(angle)
            return Point2D(self.x / math.sin(angle), self.y / math.cos(angle))

    def set_og(self, x: float, y: float):
        self._og = (x, y)

    def distance_to(self, other) -> float:
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2
        )
    
    def raw_coordinate(self):
        return self.x, self.y
    
    def shift_x(self, val: int, in_place: bool = True, return_new: bool = False):
        if in_place:
            self._x += val
        if return_new:
            return Point2D(self.x + val, self.y)
    
    def shift_y(self, val: int, in_place: bool = True, return_new: bool = False):
        if in_place:
            self._y += val
        if return_new:
            return Point2D(self.x + val, self.y)
    
    def __eq__(self, other) -> bool:
        if self.primary != "angle":
            return self.x == other.x and self.y == other.y
        else:
            return Fundamental2D.direction(Point2D(*self._og), self, other) == 0

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
                return self.y < other.y
        elif self.primary == "x_flip":
            if self.x != other.x:
                return self.x > other.x
            else:
                return self.y < other.y
        elif self.primary == "y_flip":
            if self.y != other.y:
                return self.y > other.y
            else:
                return self.y < other.y
        elif self.primary == "circumnavigation":
            line1: Line2D = Line2D.from_fix_points(Point2D(*self._og), self)
            line2: Line2D = Line2D.from_fix_points(Point2D(*self._og), other)
            m1 = line1.to_slope_intercept()
            m2 = line1.to_slope_intercept()
            return m1 < m2
        elif self.primary == "angle":
            return Fundamental2D.direction(Point2D(*self._og), self, other) == -1

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
        self._coef_a = a
        self._coef_b = b
        self._coef_c = c
    @property
    def coef_a(self):
        return self._coef_a

    @property
    def coef_b(self):
        return self._coef_b
    
    @property
    def coef_c(self):
        return self._coef_c
    
    @property
    def coefs(self):
        return self.coef_a, self.coef_b, self.coef_c
    
    def from_slop_intercept(m: int, intercept: int, is_raw: bool = False):
        a = m
        b = -1
        c = -intercept
        if is_raw:
            return a, b, c
        else:
            return Line2D(a, b, c)
    
    def from_fix_points(p1: Point2D, p2: Point2D, is_raw: bool = False):
        a =  p2.y - p1.y
        b = p1.x - p2.x
        c = (p2.x * p1.y) - (p1.x * p2.y)
        if is_raw:
            return a, b, c
        else:
            return Line2D(a, b, c)

    def to_slope_intercept(self) -> Tuple[int, int]:
        if self.coef_b != 0:
            m = -self.coef_a / self.coef_b
            intercept = -self.coef_c / self.coef_b
        else: 
            return None, None
        return m, intercept

    def distance_to(self, p: Point2D) -> float:
        top = abs(self.coef_a * p.x + self.coef_b * p.y + self.coef_c) 
        bot = math.sqrt(self.coef_a**2 + self.coef_b**2)
        d = top / bot
        return d
    
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
    def __init__(self, p1: Point2D, p2: Point2D):
        Checker.check_overlap_point(p1, p2)
        if p1 > p2:
            p1, p2 = p2, p1
        self._p1 = p1 # small
        self._p2 = p2 # large
        a, b, c = Line2D.from_fix_points(p1, p2, True)
        super().__init__(a, b, c)

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2
    
    @property
    def xy(self):
        return self.p1.xy, self.p2.xy
    
    def length(self) -> float:
        return self.p1.distance_to(self.p2)

    def connection(self) -> list[Point2D]:
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
        return Line2D
    
    def __repr__(self) -> str:
        return f"{self.p1} - {self.p2}"
    
    def __iter__(self):
        return iter([self.p1, self.p2])

class CoordinateSys2D:
    def __init__(self, points: list | list[Point2D] | np.ndarray, primary: str = "x", angle: int = 0, og: Tuple[int, int] = (0, 0), from_raw_points: bool = True):
        Checker.check_primary_point(primary)
        self._primary = primary
        Checker.check_angle(angle)
        self._angle = angle
        if from_raw_points:
            self._points = np.array(Point2D.to_points(points, primary, angle,))
        else:
            self._points = points
        unique = []
        for p in self._points:
            if not p in unique:
                unique.append(p)
        self._points = np.array(unique)
        self._og = og

    @property
    def points(self):
        return self._points
    
    @property
    def primary(self):
        return self._primary
    
    @property
    def angle(self):
        return self._angle

    @property
    def og(self):
        return self._og
        
    def rotate(self, angle: int):
        for idx in range(len(self.points)):
            self.points[idx].rotate(angle)
        self._angle = angle
    
    def set_og(self, x: float, y: float):
        self._og = (x, y)
        for idx in range(len(self.points)):
            self.points[idx].set_og(x, y)

    def set_primary(self, primary: str):
        if primary == "angle":
            self.set_og(*np.min(self.points, axis=0))
        for idx in range(len(self.points)):
            self.points[idx].set_primary(primary)
        self._primary = primary

    def sort_points(self, descending: bool = False, in_place: bool = True):
        res = np.sort(self.points, kind = "heapsort")
        if descending:
            res = np.flip(res)
        if in_place:
            self._points = res
        else:
            return res
    
    def is_points_sorted(self) -> bool:
        return np.all(self.points[:-1] <= self.points[1:])

    def draw_graph(self) -> list:
        self.sort_points()
        graph = []
        for idx in range(len(self.points)-1):
            p1, p2 = Point2D(*self.points[idx]), Point2D(*self.points[idx+1])
            graph += Segment2D(p1, p2).connection()[:-1:] 
        return graph

    def draw_polygon(self, dividing_line: int | Line2D = -1, as_segment: bool = True) -> list[Segment2D] | list[Point2D]:
        self.sort_points()
        if dividing_line == -1:
            last_primary = self._primary
            self.set_primary("y")
            points = self.sort_points(in_place = False)
            self.set_primary(last_primary)
            dividing_line = Line2D(
                a = 0,
                b = 1,
                c = -points[len(points)//2].y
            )
        elif isinstance(dividing_line, int):
            dividing_line = Line2D(
                a = 0,
                b = 1,
                c = -dividing_line
            )
        raw_p = dividing_line.x_y_range(0, 2)
        dp1 = Point2D(*raw_p[0])
        dp2 = Point2D(*raw_p[1])
        
        border: list[Segment2D]  = []
        points = []
        # upper hull
        points = [p for p in self.points if Fundamental2D.direction(dp1, dp2, p) <= 0]
        sorted(points)
        for idx in range(len(points)-1):
            p1, p2 = Point2D(*points[idx]), Point2D(*points[idx+1])
            border.append(Segment2D(p1, p2))
            
        points= []
        # lower hull
        points = [p for p in self.points if Fundamental2D.direction(dp1, dp2, p) > 0]
        sorted(points)
        points.reverse()
        
        border.append(Segment2D(
            Point2D(*border[-1].p2),
            Point2D(*points[0])
        ))
        
        for idx in range(len(points)-1):
            p1, p2 = Point2D(*points[idx]), Point2D(*points[idx+1])
            border.append(Segment2D(p1, p2))

        border.append(Segment2D(
            Point2D(*border[0].p1),
            Point2D(*border[-1].p1)
        ))

        if as_segment:
            return border
        
        graph = []
        for p in border:
            graph += p.connection()[:-1:]
        return graph

    def __repr__(self) -> str:
        return f"{self.points}"
    
    def __iter__(self):
        return iter(self.points)
    
    def __len__(self):
        return len(self.points)
